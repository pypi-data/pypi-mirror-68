import logging

from future import standard_library
from opentracing import tags

from ._patcher import Patcher
from ..http_client import AbstractRequestWrapper, \
    before_http_request, split_host_and_port

standard_library.install_aliases()

log = logging.getLogger(__name__)

try:
    import aiohttp
except ImportError:
    pass
else:
    _ClientSession__init__ = aiohttp.ClientSession.__init__


class AioHTTPClientSessionPatcher(Patcher):
    applicable = '_ClientSession__init__' in globals()
    response_handler_hook = None

    def _install_patches(self):
        aiohttp.ClientSession.__init__ = self._get_client_session_wrapper()

    def _reset_patches(self):
        aiohttp.ClientSession.__init__ = _ClientSession__init__

    def set_response_handler_hook(self, response_handler_hook):
        """
        Set a hook that will be called when a response is received.

        The hook can be set in purpose to set custom tags to spans
        depending on content or some metadata of responses.

        :param response_handler_hook: hook method
            It must have a signature `(response, span)`,
            where `response` and `span` are positional arguments,
            so you can use different names for them if needed.
        """

        self.response_handler_hook = response_handler_hook

    def _get_client_session_wrapper(self):
        def tracing_wrapper(*args, **kwargs):
            trace_configs = kwargs.get('trace_configs', [])

            trace_config = aiohttp.TraceConfig()
            trace_config.on_request_start.append(self._get_on_request_start())
            trace_config.on_request_end.append(self._get_on_request_end())

            trace_configs.append(trace_config)

            kwargs['trace_configs'] = trace_configs

            return _ClientSession__init__(*args, **kwargs)

        return tracing_wrapper

    def _get_on_request_start(self):
        async def on_request_start(session, context,
                                   params):
            request_wrapper = self.RequestWrapper(request=params)
            context.span = before_http_request(
                request=request_wrapper,
            )

        return on_request_start

    def _get_on_request_end(self):
        async def on_request_end(session, context,
                                 params: aiohttp.TraceRequestEndParams):
            if getattr(context, 'span', None) is not None:
                span = context.span

                response = params.response
                if getattr(response, 'status', None) is not None:
                    span.set_tag(tags.HTTP_STATUS_CODE, response.status)
                if self.response_handler_hook is not None:
                    self.response_handler_hook(response, span)

                span.finish()

        return on_request_end

    class RequestWrapper(AbstractRequestWrapper):
        def __init__(self, request):
            self.request = request
            self.scheme = request.url.scheme
            self.host_str = request.url.host

        def add_header(self, key, value):
            self.request.headers[key] = value

        @property
        def method(self):
            return self.request.method

        @property
        def full_url(self):
            return self.request.url

        @property
        def _headers(self):
            return self.request.headers

        @property
        def host_port(self):
            return split_host_and_port(host_string=self.host_str,
                                       scheme=self.scheme)


AioHTTPClientSessionPatcher.configure_hook_module(globals())

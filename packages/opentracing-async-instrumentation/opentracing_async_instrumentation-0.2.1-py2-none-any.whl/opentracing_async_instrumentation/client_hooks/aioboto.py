import asyncio
import sys

import opentracing
from opentracing import tags
import wrapt

from opentracing_async_instrumentation.client_hooks._patcher import Patcher
from ..utils import unwrap

ARGS_NAME = ('action', 'params', 'path', 'verb')
TRACED_ARGS = ['params', 'path', 'verb']

PYTHON_VERSION_INFO = sys.version_info

try:
    import aiobotocore
    from aiobotocore.client import AioBaseClient
    from botocore.exceptions import ClientError

    # This was moved in aiobotocore 0.11.0
    try:
        from aiobotocore.endpoint import ClientResponseContentProxy
    except ImportError:
        from aiobotocore._endpoint_helpers import ClientResponseContentProxy
except ImportError:
    pass
else:
    _client_make_api_call = AioBaseClient._make_api_call


class AioBotoPatcher(Patcher):
    applicable = '_client_make_api_call' in globals()

    def __init__(self):
        super(AioBotoPatcher, self).__init__()

    def _install_patches(self):
        if getattr(aiobotocore.client, '_opentracing_patch', False):
            return
        setattr(aiobotocore.client, '_opentracing_patch', True)

        wrapt.wrap_function_wrapper('aiobotocore.client',
                                    'AioBaseClient._make_api_call',
                                    _wrapped_api_call)

    def _reset_patches(self):
        if getattr(aiobotocore.client, '_opentracing_patch', False):
            setattr(aiobotocore.client, '_opentracing_patch', False)
            unwrap(aiobotocore.client.AioBaseClient, '_make_api_call')


class WrappedClientResponseContentProxy(wrapt.ObjectProxy):
    def __init__(self, body, parent_span):
        super(WrappedClientResponseContentProxy, self).__init__(body)
        self._self_parent_span = parent_span

    @asyncio.coroutine
    def read(self, *args, **kwargs):
        # async read that must be child of the parent span operation
        operation_name = '{}.read'.format(self._self_parent_span.name)

        with opentracing.global_tracer().start_active_span(
                operation_name=operation_name,
                child_of=self._self_parent_span) as span:
            # inherit parent attributes
            span.resource = self._self_parent_span.resource
            span.span_type = self._self_parent_span.span_type
            span.meta = dict(self._self_parent_span.meta)

            result = yield from self.__wrapped__.read(*args, **kwargs)
            span.set_tag('Length', len(result))

        return result

    # wrapt doesn't proxy `async with` context managers
    if PYTHON_VERSION_INFO >= (3, 5, 0):
        @asyncio.coroutine
        def __aenter__(self):
            # call the wrapped method but return the object proxy
            yield from self.__wrapped__.__aenter__()
            return self

        @asyncio.coroutine
        def __aexit__(self, *args, **kwargs):
            response = yield from self.__wrapped__.__aexit__(*args, **kwargs)
            return response


def _set_request_id_tag(span, response):
    metadata = response.get('ResponseMetadata')

    # there is no ResponseMetadata for
    # aiobotocore:dynamodb:describe_table
    if metadata:
        request_id = metadata.get('RequestId')

        # when using aiobotocore.client('s3')
        # instead of aiobotocore.resource('s3'),
        # there is no RequestId for
        # aiobotocore:s3:CreateBucket
        if request_id:
            span.set_tag('aws.request_id', request_id)


@asyncio.coroutine
def _wrapped_api_call(original_func, instance, args, kwargs):
    service_name = instance._service_model.service_name
    endpoint = instance._endpoint._endpoint_prefix
    region = instance.meta.region_name
    operation_name = args[0]

    tracer = opentracing.global_tracer()

    span = tracer.start_span(
        operation_name='aiobotocore:client:{}:{}:{}'.format(
            service_name, endpoint, operation_name
        ),  # noqa
    )

    if len(args) > 0:
        operation = args[0]
        span.resource = '{}.{}'.format(endpoint, operation.lower())
    else:
        span.resource = endpoint

    span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_CLIENT)
    span.set_tag(tags.COMPONENT, 'aiobotocore')
    span.set_tag('aiobotocore.service_name', service_name)
    span.set_tag('aws.region', region)

    with span:
        try:
            result = yield from original_func(*args, **kwargs)
        except ClientError as error:
            _set_request_id_tag(span, error.response)
            raise
        except Exception:
            raise
        else:
            if isinstance(result, dict):
                _set_request_id_tag(span, result)

        body = result.get('Body')
        if isinstance(body, ClientResponseContentProxy):
            result['Body'] = WrappedClientResponseContentProxy(body, span)

        response_meta = result['ResponseMetadata']
        response_headers = response_meta['HTTPHeaders']

        span.set_tag('status_code', response_meta['HTTPStatusCode'])
        span.set_tag('retry_attempts', response_meta['RetryAttempts'])

        request_id2 = response_headers.get('x-amz-id-2')
        if request_id2:
            span.set_tag('aws.request_id2', request_id2)

        return result


AioBotoPatcher.configure_hook_module(globals())

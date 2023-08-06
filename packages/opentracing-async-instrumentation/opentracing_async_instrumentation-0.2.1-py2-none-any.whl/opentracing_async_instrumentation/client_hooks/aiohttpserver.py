import asyncio
from typing import TypeVar

import opentracing

from ..http_server import AbstractRequestWrapper, before_request

_Func = TypeVar('_Func')


def __middleware(f: _Func) -> _Func:
    f.__middleware_version__ = 1  # type: ignore
    return f


class AioHTTPRequestWrapper(AbstractRequestWrapper):
    """
    Wraps aiohttp.web.Request and exposes several properties used by the
    tracing methods.
    """

    def __init__(self, request):
        self.request = request

    @property
    def full_url(self):
        return self.request.url.human_repr()

    @property
    def headers(self):
        return self.request.headers

    @property
    def method(self):
        return self.request.method

    @property
    def remote_ip(self):
        return self.request.remote


@__middleware
async def enable_tracing(request, handler):
    span = before_request(AioHTTPRequestWrapper(request))

    with opentracing.global_tracer().scope_manager.activate(span, True):
        resp = await handler(request)

        if asyncio.iscoroutine(resp):
            resp = await resp

        return resp

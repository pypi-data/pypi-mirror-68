# Copyright (c) 2015 Uber Technologies, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from builtins import object

import opentracing
from future import standard_library
from opentracing import Format
from opentracing.ext import tags

from . import config

standard_library.install_aliases()


class AbstractRequestWrapper(object):
    """
    Exposes several properties used by the tracing methods.
    """

    @property
    def caller_name(self):
        for header in config.CONFIG.caller_name_headers:
            caller = self.headers.get(header.lower(), None)
            if caller is not None:
                return caller
        return None

    @property
    def full_url(self):
        raise NotImplementedError('full_url')

    @property
    def headers(self):
        raise NotImplementedError('headers')

    @property
    def method(self):
        raise NotImplementedError('method')

    @property
    def remote_ip(self):
        raise NotImplementedError('remote_ip')

    @property
    def remote_port(self):
        return None

    @property
    def server_port(self):
        return None

    @property
    def operation(self):
        return self.method


def before_request(request: AbstractRequestWrapper, tracer=None):
    """
    Attempts to extract a tracing span from incoming request.
    If no tracing context is passed in the headers, or the data
    cannot be parsed, a new root span is started.

    :param request: HTTP request with `.headers` property exposed
        that satisfies a regular dictionary interface
    :param tracer: optional tracer instance to use. If not specified
        the global opentracing.tracer will be used.
    :return: returns a new, already started span.
    """

    if tracer is None:
        tracer = opentracing.global_tracer()

    span_context = tracer.extract(
        format=Format.HTTP_HEADERS,
        carrier=request.headers,
    )

    span = tracer.start_span(
        operation_name=request.operation,
        child_of=span_context,
    )

    span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_SERVER)

    span.set_tag(tags.HTTP_URL, request.full_url)
    span.set_tag(tags.HTTP_METHOD, request.method)

    remote_ip = request.remote_ip
    if remote_ip:
        span.set_tag(tags.PEER_HOST_IPV4, remote_ip)

    caller_name = request.caller_name
    if caller_name:
        span.set_tag(tags.PEER_SERVICE, caller_name)

    remote_port = request.remote_port
    if remote_port:
        span.set_tag(tags.PEER_PORT, remote_port)

    return span

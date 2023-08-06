[![PyPI version][pypi-img]][pypi] [![Python versions][pyver-img]][pypi] [![Pypi Downloads][pydl-img]][pypi] [![Build Status][ci-img]][ci] [![Coverage Status][cov-img]][cov]


# python-opentracing-async-instrumentation

A collection of asyncio instrumentation tools to enable tracing with [OpenTracing API](http://opentracing.io).

## Module

Make sure you are running recent enough versions of `pip` and `setuptools`, e.g. before installing your project requirements execute this:

```
pip install --upgrade "setuptools>=29" "pip>=9"
```

The module name is `opentracing_async_instrumentation`.

## What's inside

### Supported client frameworks

The following libraries are instrumented for tracing in this module:
 * [aiobotocore](https://github.com/aio-libs/aiobotocore) — Asyncio AWS SDK for Python
 * [aioboto3](https://github.com/terrycain/aioboto3) — Asyncio AWS SDK for Python (uses aiobotocore under the hood)
 * [aiohttp](https://github.com/aio-libs/aiohttp/) - Asyncio HTTP server and client
 * [aiomysql](https://github.com/aio-libs/aiomysql)

#### Limitations

 * Only Python 3.5+ is currently supported.

### Server instrumentation

For inbound requests a helper function `before_request` is provided for creating middleware for frameworks like aiohttp and possibly Tornado.

A middleware is provided for `aiohttp`.

### In-process Context Propagation

As part of the OpenTracing 2.0 API, in-process `Span` propagation happens through the newly defined
[ScopeManager](https://opentracing-python.readthedocs.io/en/latest/api.html#scope-managers)
interface.

## Usage

This library provides two types of instrumentation, explicit instrumentation
for server endpoints, and implicit instrumentation for client call sites.

### Server

Server endpoints are instrumented by creating a (or using a provided) middleware class that:

 1. initializes the specific tracer implementation
 2. wraps incoming request handlers into a method that reads the incoming
    tracing info from the request and creates a new tracing Span

```python
from aiohttp import web
from opentracing_async_instrumentation.client_hooks import aiohttpserver

async def handler(request):
    return web.Response(body='Hello World')

app = web.Application()
app.router.add_get('/', handler)
app.middlewares.append(aiohttpserver.enable_tracing)

if __name__ == '__main__':
    web.run_app(app)
```

### Client

Client call sites are instrumented implicitly by executing a set of
available `client_hooks` that monkey-patch some API points in several
common libraries like `aiohttp` and `aiobotocore`. The initialization of
those hooks is usually also done from the middleware class's `__init__` method.

Usage is via the `client_hooks` interface.

```python
from opentracing_async_instrumentation import client_hooks

client_hooks.install_all_patches()
```

### Customization

For the `aiohttp` library, in case you want to set custom tags
to spans depending on content or some metadata of responses,
you can set `response_handler_hook`.
The hook must be a method with a signature `(response, span)`,
where `response` and `span` are positional arguments,
so you can use different names for them if needed.

```python
from opentracing_async_instrumentation.client_hooks.aiohttpclient import patcher


def hook(response, span):
    if not response.ok:
        span.set_tag('error', 'true')


patcher.set_response_handler_hook(hook)
```

## Development

To prepare a development environment please execute the following commands.
```bash
virtualenv env
source env/bin/activate
make bootstrap
make test
```

You can use [tox](https://tox.readthedocs.io) to run tests as well.
```bash
tox
```

[ci-img]: https://gitlab.com/midigator/python_opentracing_async_instrumentation/badges/master/pipeline.svg
[ci]: https://gitlab.com/midigator/python_opentracing_async_instrumentation
[pypi-img]: https://img.shields.io/pypi/v/opentracing_async_instrumentation.svg
[pypi]: https://pypi.python.org/pypi/opentracing_async_instrumentation
[cov-img]: https://gitlab.com/midigator/python_opentracing_async_instrumentation/badges/master/coverage.svg
[cov]: https://gitlab.com/midigator/python_opentracing_async_instrumentation/badges/master/coverage.svg
[pyver-img]: https://img.shields.io/pypi/pyversions/opentracing-async-instrumentation.svg
[pydl-img]: https://img.shields.io/pypi/dm/opentracing-async-instrumentation.svg

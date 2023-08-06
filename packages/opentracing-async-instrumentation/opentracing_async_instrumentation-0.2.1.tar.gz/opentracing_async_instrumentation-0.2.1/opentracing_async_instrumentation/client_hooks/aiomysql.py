# Copyright (c) 2015,2019 Uber Technologies, Inc.
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

from __future__ import absolute_import

from ._dbapi2_async import ConnectionFactory
from ._dbapi2_async import ContextManagerConnectionWrapper as ConnectionWrapper
from ._patcher import Patcher

# Try to save the original entry points
try:
    import aiomysql
except ImportError:
    pass
else:
    _aiomysql_connect = aiomysql.connect


class MySQLdbPatcher(Patcher):
    applicable = '_aiomysql_connect' in globals()

    def _install_patches(self):
        factory = ConnectionFactory(connect_func=aiomysql.connect,
                                    module_name='aiomysql',
                                    conn_wrapper_ctor=ConnectionWrapper)

        if hasattr(aiomysql, 'connect'):
            aiomysql.connect = factory

        if hasattr(aiomysql.pool, 'connect'):
            aiomysql.pool.connect = factory

    def _reset_patches(self):
        if hasattr(aiomysql, 'connect'):
            aiomysql.connect = _aiomysql_connect

        if hasattr(aiomysql.pool, 'connect'):
            aiomysql.pool.connect = _aiomysql_connect


MySQLdbPatcher.configure_hook_module(globals())

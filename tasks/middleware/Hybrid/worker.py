from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer
import redis
import sys
import pandas as pd


master = redis.Redis(port=16379)

port = sys.argv[1]
url = 'http://localhost:' + str(port)

master.hmset("urls", url)

# Restrict master particular path
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create master server
with SimpleXMLRPCServer(('localhost', int(port)), allow_none=True,
                    requestHandler=RequestHandler) as server:
    server.register_introspection_functions()


    class WorkerAPI:
        df = None

        def read_csv(self, s):
            self.df = pd.read_csv(s)

        def apply(self, func, axis=0, broadcast=None, raw=False, reduce=None,
                    result_type=None, args=(), **kwds):
            return format(self.df.apply(func, axis, broadcast, raw, reduce, result_type, args, kwds))

        def columns(self):
            return format(self.df.columns)

        def groupby(self, by=None, axis=0, level=None, as_index=True, sort=True):
            return format(self.df.groupby(by, axis, level, as_index, sort))

        def head(self, n):
            return format(self.df.head(n))

        def isin(self, label, value):
            return self.df[label].isin(value)

        def items(self):
            dictionary = dict()
            for label, content in self.df.items():
                dictionary[label] = content
            return format(dictionary)

        def max(self, s):
            return format(self.df.max(s, numeric_only=True))
        
        def min(self, s):
            return format(self.df.min(s, numeric_only=True))

    server.register_instance(WorkerAPI())

    server.serve_forever()
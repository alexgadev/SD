from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer
import xmlrpc.client
import sys
import pandas as pd


master = xmlrpc.client.ServerProxy('http://localhost:8000')

port = sys.argv[1]
url = 'http://localhost:' + str(port)

master.addWorker(url)

# Restrict worker particular path
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create worker server
with SimpleXMLRPCServer(('localhost', int(port)), allow_none=True,
                    requestHandler=RequestHandler) as server:
    server.register_introspection_functions()


    class WorkerAPI:
        df = None

        #
        def read_csv(self, s):
            self.df = pd.read_csv(s)

        
        def apply(self, func, axis=0, reduce=None, result_type=None, args=()):
            da = self.df.apply(lambda x: str(x), axis, reduce, result_type, args)
            print(da)
            print(str(func))
            return format(self.df.apply(func, axis, reduce, result_type, args))

        #
        def columns(self):
            return format(self.df.columns)

        # must pass a function to do groupby().func
        def groupby(self, by=None, axis=0, level=None, as_index=True, sort=True):
            return format(self.df.groupby(by, axis, level, as_index, sort))

        # pass a number
        def head(self, n):
            return format(self.df.head(n))

        # two different ways isin(values) or the other writen
        def isin(self, values, label):
            new = self.df[label].isin(values)
            return format(self.df[new])

        #
        def items(self):
            dictionary = dict()
            for label, content in self.df.items():
                dictionary[label] = content
            return format(dictionary)

        #
        def max(self, s):
            return format(self.df.max(s, numeric_only=True))
        
        #
        def min(self, s):
            return format(self.df.min(s, numeric_only=True))

    server.register_instance(WorkerAPI())

    server.serve_forever()
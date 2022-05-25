from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from random import seed
from random import randint

# Restrict to a particular path
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
with SimpleXMLRPCServer(('localhost', 8000), allow_none=True, 
                    requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    class Funcs:
        seed(1)
        list = ['bobo']

        def addInsult(self, s):
            self.list.append(s)

        def getInsults(self):
            return self.list

        def insultMe(self):
            n = randint(0, len(self.list))
            return self.list[n]
    
    server.register_instance(Funcs())

    # Run the server's main loop
    server.serve_forever()
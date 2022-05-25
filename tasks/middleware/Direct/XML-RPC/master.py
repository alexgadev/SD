from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer

workers = [] # list containing connection to each worker

# Restrict master path
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create master server
with SimpleXMLRPCServer(('localhost', 8000), allow_none=True,
                    requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    class MasterAPI:

        def addWorker(self, url):
            workers.append(url)

        def getWorkers(self):
            return workers

    server.register_instance(MasterAPI())

    server.serve_forever()
import xmlrpc.client

server = xmlrpc.client.ServerProxy('http://localhost:8000')

server.addInsult('tontito')
print(server.getInsults())
print(server.insultMe())
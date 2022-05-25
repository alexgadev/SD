import xmlrpc.client
import redis

master = redis.Redis(port=16379)


workersURL = master.smembers("urls")
workerList = []


print('Establishing connection with workers...')
for w in workersURL:
    url = w.decode("utf-8")
    workerList.append(xmlrpc.client.ServerProxy(url))

print('Loading csv...')
for worker in workerList:
    worker.read_csv('data.csv')

print('Getting columns...')
for elem in workerList:
    res = elem.max('columns')
    print(res)
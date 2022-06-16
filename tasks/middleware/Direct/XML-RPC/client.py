import xmlrpc.client

master = xmlrpc.client.ServerProxy('http://localhost:8000')

csv = 'data.csv'

nRows = 0
for row in open(csv):
    nRows += 1

workersURL = master.getWorkers()
workerList = []

print('Establishing connection with workers...')
for w in workersURL:
    workerList.append(xmlrpc.client.ServerProxy(w))

print('Loading csv...')
for worker in workerList:
    worker.read_csv(csv)

def caps(x):
    return str(x).capitalize

print('Grouping By Variable_code...')
for elem in workerList:
    #res = elem.max('columns')
    #res = elem.groupby('Variable_code')
    #res = elem.columns()
    #res = elem.isin([2020], 'Year')
    #res = elem.items()
    res = elem.apply(caps)
    print(res)
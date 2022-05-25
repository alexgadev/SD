import redis
import json

r = redis.Redis(host='localhost', port=6379)

msg = {'channel': 'response-channel', 'request': 'min'}

r.publish('request-channel', json.dumps(msg))
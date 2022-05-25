import json
import redis
import time
import pandas as pd

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

p = r.pubsub()
p.subscribe('request-channel')

df = None

while True:
    message = p.get_message()
    if message:
        print(message)
        if message.get('type') != 'subscribe':
            data = message.get('data')

            stud_obj = json.loads(str(data))

            print("channel: ", stud_obj['channel'], "\trequest: ", stud_obj['request'])

            match stud_obj['request']:
                case 'read_csv':
                    df = pd.read_csv(stud_obj['arg'])

                case 'apply':
                    r.hmset("apply", df.apply())

                case 'columns':
                    r.hmset("columns", )

                case 'groupby':
                    r.hmset("groupby", )

                case 'head':
                    r.hmset("head", )

                case 'isin':
                    r.hmset("head", )

                case 'items':
                    r.hmset("items", )

                case 'max':
                    r.hmset("max", )

                case 'min':
                    r.hmset("min", )
            
    time.sleep(0.01)
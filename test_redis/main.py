import datetime
import time


from fastapi import FastAPI
import redis
import json

app = FastAPI()
r = redis.Redis(host="localhost", port=6379, db=0)


def get_response(key):
    message = {"message": "Hello World"}
    if r.get(key) is None:
        time.sleep(1)
        r.set(name=key, value=json.dumps(message), ex=datetime.timedelta(seconds=30))
        response = message
    else:
        message = r.get(key).decode("utf-8")
        response = json.loads(message)
    return response


@app.get("/")
async def root():
    key = "message"
    start_time = time.time()
    response = get_response(key)
    process_time = time.time() - start_time
    print(f"process_time: {process_time}")
    return response

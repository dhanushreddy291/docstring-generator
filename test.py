import time

import redis
from flask import Flask


app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    """
    
    Increments the hit count in the cache and returns the updated count. If there is a connection error with Redis, retries up to 5 times before raising the exception. 
    
    Returns:
        int: The updated hit count in the cache.
    
    """
    retries = 5
    while True:
        try:
            return cache.incr('hits')
except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    """
    A Flask route that returns a greeting message along with the hit count retrieved from the `get_hit_count()` function.
    
    Returns:
        str: A greeting message with the hit count.
    """
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

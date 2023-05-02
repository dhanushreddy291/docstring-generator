from flask import Flask, jsonify, current_app
from flask_cors import CORS
from redis import Redis
from random import randint
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
_redis = Redis(host=os.getenv('REDIS_HOSTNAME'), port=6379, password=os.getenv("REDIS_PASSWORD")) 
_redis_pubsub = _redis.pubsub()
_redis_pubsub.subscribe('my-first-channel')

@app.before_request
def checkConnectionRedis():
    """
    This function is a Flask route that checks the connection to Redis before each request. If the connection is lost, it tries to reconnect to Redis and subscribes to a channel. The function logs information about the request using the Flask logger.
    """
    global _redis, _redis_pubsub
    current_app.logger.info("---before_request---")
    try:
        _redis.ping()
    except _redis.ConnectionError:
        redis = Redis(host='redis', port=6379)
        _redis_pubsub = _redis.pubsub()
        _redis_pubsub.subscribe('my-first-channel')

def getcounter():
    """
    This Python function retrieves the value of a counter from Redis and returns it as an integer. If the counter does not exist in Redis, it returns 0. The function uses the Redis `get` method to retrieve the counter value and decodes it from bytes to a string before converting it to an integer.
    """
    return _redis.get('web_counter') and int(_redis.get('web_counter').decode("utf-8")) or 0

@app.route('/counter', methods=["GET"])
def get():
    """
    This Flask route returns the current value of a counter as a JSON object. The route uses the `getcounter` function to retrieve the counter value from Redis and returns it as a JSON object with the key `web_counter`. The route only accepts GET requests.
    """
    return jsonify(web_counter=getcounter())

@app.route('/counter', methods=["POST"])
def create():
    """
    This Flask route increments the value of a counter in Redis by 1 and returns an empty string. The route uses the Redis `incr` method to increment the counter value. The route only accepts POST requests.
    """
    _redis.incr('web_counter')
    return ""

@app.route('/counter', methods=["DELETE"])
def remove():
    """
    This Flask route resets the value of a counter in Redis to 0 and returns an empty string. The route uses the Redis `set` method to set the counter value to 0. The route only accepts DELETE requests.
    """
    _redis.set('web_counter', 0)
    return ""

@app.route('/message', methods=["GET"])
def getMessage():
    """
    This Flask route retrieves a message from a Redis pub/sub channel and returns it as a JSON object. The route logs information about the received message using the Flask logger. The route uses the Redis `get_message` method to retrieve the message from the pub/sub channel and returns it as a JSON object with the key `message`. The route only accepts GET requests.
    """
    current_app.logger.info("recieve data: " + str(_redis_pubsub.get_message()))
    return jsonify(message=str(_redis_pubsub.get_message()))

@app.route('/message', methods=["POST"])
def createMessage():
    """
    This Flask route publishes a message to a Redis pub/sub channel and returns an empty string. The message is generated randomly using the `randint` function. The route logs information about the published message using the Flask logger. The route uses the Redis `publish` method to publish the message to the pub/sub channel. The route only accepts POST requests.
    """
    data = 'data ' + str(randint(0,10))
    current_app.logger.info("publish data: " + str(data))
    _redis.publish('my-first-channel', data)
    return ""

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

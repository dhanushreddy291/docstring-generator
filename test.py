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
    global _redis, _redis_pubsub
    current_app.logger.info("---before_request---")
    try:
        _redis.ping()
    except _redis.ConnectionError:
        redis = Redis(host='redis', port=6379)
        _redis_pubsub = _redis.pubsub()
        _redis_pubsub.subscribe('my-first-channel')

def getcounter():
    return _redis.get('web_counter') and int(_redis.get('web_counter').decode("utf-8")) or 0

@app.route('/counter', methods=["GET"])
def get():
    return jsonify(web_counter=getcounter())

@app.route('/counter', methods=["POST"])
def create():
    _redis.incr('web_counter')
    return ""

@app.route('/counter', methods=["DELETE"])
def remove():
    _redis.set('web_counter', 0)
    return ""

@app.route('/message', methods=["GET"])
def getMessage():
    current_app.logger.info("recieve data: " + str(_redis_pubsub.get_message()))
    return jsonify(message=str(_redis_pubsub.get_message()))

@app.route('/message', methods=["POST"])
def createMessage():
    data = 'data ' + str(randint(0,10))
    current_app.logger.info("publish data: " + str(data))
    _redis.publish('my-first-channel', data)
    return ""

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
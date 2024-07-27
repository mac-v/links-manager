import time
import logging
from flask import Flask, jsonify

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route('/api/time')
def get_current_time():
    app.logger.info("/api/time handled")
    return jsonify({'time': time.time()})
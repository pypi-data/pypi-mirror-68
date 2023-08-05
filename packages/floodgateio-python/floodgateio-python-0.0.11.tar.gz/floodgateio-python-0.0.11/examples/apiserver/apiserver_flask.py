
from flask import Flask
from floodgateio.floodgate_client import FloodGateClient
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


app = Flask(__name__)
features = FloodGateClient.initialize_from_key_autoupdate("2bd051da88585d91dd6eae445f6db915975d48d387d6205d2a52692dde75")


@app.route('/')
def hello_world():
    feature_flag = features.get_value("welcome-greeting-v3", False)
    if feature_flag:
        text = 'Hello, New World!'
    else:    
        text = 'Hello, World!'
    return text

if __name__ == '__main__':
    app.debug = True
    app.run('127.0.0.1', port=5000)

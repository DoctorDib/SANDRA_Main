import json
CONFIG = {}

def setup():
    with open('./config.json') as f:
        global CONFIG
        CONFIG = json.load(f)
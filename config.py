import json
import os

CONFIG = {}

def setup():
    with open(os.path.join(os.getcwd(), 'config.json')) as f:
        global CONFIG
        CONFIG = json.load(f)
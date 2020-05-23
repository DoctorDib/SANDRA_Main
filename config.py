import json
import os

CONFIG = {}

def setup():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 'config.json')) as f:
        global CONFIG
        CONFIG = json.load(f)
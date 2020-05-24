from os.path import abspath, dirname

import json
import os

CONFIG = {}

def setup():
    current_dir = dirname(abspath(__file__))

    with open(os.path.join(current_dir, 'config.json')) as f:
        global CONFIG
        CONFIG = json.load(f)
        CONFIG["directory"]["main"] = current_dir
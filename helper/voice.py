import pyttsx3
import config

global engine

def setup():
    global engine
    engine = pyttsx3.init() # object creation
    engine.setProperty('rate', config.CONFIG["bot_voice"]["rate"])     # setting up new voice rate
    engine.setProperty('volume', config.CONFIG["bot_voice"]["volumne"])    # setting up volume level  between 0 and 1

    """VOICE"""
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[config.CONFIG["bot_voice"]["voice_id"]].id)   #changing index, changes voices. 1 for female

def say(text):
    engine.say(text)
    engine.runAndWait()
    engine.stop()
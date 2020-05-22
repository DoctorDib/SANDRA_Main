
from textblob.classifiers import NaiveBayesClassifier
from helper import input_control as input

import pickle

TEST_DATA = [
    "what is it is sandra",
    "can you remind me in 5 minutes to start cooking sandra",
    "sandra can you turn the lights on in the kitchen please",
    "sandra can you remind me to do the shopping at 5",
    "do you happen to know the time sandra",
    "what is the current hour sandra"
]

f = open('models/recognition.pickle', 'rb')
classifier = pickle.load(f)

for val in TEST_DATA:

    pro = input.mlp(val)

    print(val + " || " + classifier.classify(pro))
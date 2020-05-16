
from textblob.classifiers import NaiveBayesClassifier
from helper import input_control as input

import pickle

TRAIN_DATA = [

#REQUEST
    (input.mlp("sandra can you please set the timer for 5 seconds"), 'request'),
    (input.mlp("can you please set the timer for 5 seconds sandra"), 'request'),

    (input.mlp("hey sandra can you remind me to goto the shops in 5 minutes"), 'request'),
    (input.mlp("can you remind me to goto the shops in 5 minutes sandra"), 'request'),

    (input.mlp("sandra remind me to go to the shops at 5"), 'request'),
    (input.mlp("remind me to go to the shops at 5 sandra"), 'request'),

# QUESTION
    (input.mlp("sandra what time is it"), 'question'),
    (input.mlp("what time is it sandra"), 'question'),

    (input.mlp("whats the time sandra"), 'question'),
    (input.mlp("sandra whats the time"), 'question'),

    (input.mlp("what is the time sandra"), 'question'),
    (input.mlp("sandra what is the time"), 'question'),

    (input.mlp("sandra do you happen to know the time"), 'question'),
    (input.mlp("do you happen to know the time sandra"), 'question'),

    (input.mlp("what is the weather like sandra"), 'question'),
    (input.mlp("sandra what is the weather like"), 'question'),

# ACTION
    (input.mlp("sandra can you turn on the lights please"), 'action'),
    (input.mlp("can you turn on the lights please sandra"), 'action'),

    (input.mlp("sandra turn the heating on"), 'action'),
    (input.mlp("turn the heating on sandra"), 'action'),

    (input.mlp("hello sandra"), 'greet'),
    (input.mlp("hi sandra"), 'greet'),
    (input.mlp("morning sandra"), 'greet'),

    (input.mlp("night sandra"), 'part'),
    (input.mlp("bye sandra"), 'part'),
    (input.mlp("see you later sandra"), 'part'),
    (input.mlp("cheerio sandra"), 'part'),
]

cl = NaiveBayesClassifier(TRAIN_DATA)

## saving
f = open('recognition.pickle', 'wb')
pickle.dump(cl, f)

f.close()
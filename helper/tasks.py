from tasks import action_handler
from tasks import question_handler
from tasks import request_handler
from tasks import greet_part_handler

import pickle
import os
import config

f =open(os.path.join(config.CONFIG["directory"]["main"], 'models/recognition.pickle'), 'rb')
classifier = pickle.load(f)

def ProcessTask(req, pro, input):
    classify_sentence = classifier.classify(pro)

    if (classify_sentence == "question"):
        return question_handler.Process(req, pro, input)
    elif (classify_sentence == "request"):
        return request_handler.Process(req, pro, input)
    elif (classify_sentence == "action"):
        return action_handler.Process(req, pro, input)
    elif (classify_sentence == "greet" or classify_sentence == "part"):
        return greet_part_handler.Process(classify_sentence, req, pro, input)
    else:
        print("ERROR")
        return "There happens to be an error."
#!/usr/bin/env python3
from helper import voice
from helper import input_control

import speech_recognition as sr
import threading
import time

import config
import socket
import json
import sys

import asyncore
import logging

global task_socket

r = sr.Recognizer()  
useVoice = False

#arg = sys.argv[1]

device_key = ''

if (len(sys.argv) == 2):
    device_key = sys.argv[1]
else:
    device_key = socket.gethostname()

logger = []

HOST = "localhost"
PORT = 65432
INFO_PORT = 65433

info_socket = False

def log(*args):
    global logger
    global info_socket

    final = ""

    for arg in args:
        if (type(arg) == 'dict'):
            final = final + "'" + json.dumps(arg) + "'"
        else:
            final = final + str(arg)
    
    if (len(logger) > config.CONFIG['log']['max_limit']):
        del logger[0]

    logType = ''

    if ('Error:' in final):
        logType = 'Error'
    else: 
        logType = 'Info'

    print(final)
    logger.append({'logType': logType, 'message': final})
    
    send_info_update()

def send_info_update():
    global logger

    if (info_socket):
        json_content = {
            'ID': device_key,
            'logger': logger
        }

        to_send = json.dumps(json_content).encode('utf-8')

        info_socket.send(to_send)  # send updated infomation

def send_task_socket(socket_type, message, wait_for_response):
    global logger

    json_content = {
        'ID': device_key,
        'type': socket_type,
        'content': message,
        'logger': logger
    }

    to_send = json.dumps(json_content).encode('utf-8')

    task_socket.send(to_send)  # send message

    if (wait_for_response):
        raw_data = task_socket.recv(1024)
        
        if (raw_data):
            return json.loads(raw_data)

    return {}

def handle_response(response):
    global task_socket

    log("Info: ", response)
    
    try:
        if (response == {}):
            return

        if (response['type'] == 'heartbeat'):
            send_task_socket('heartbeat', '', True)
        elif(response['type'] == 'voice_response'):
            voice.say(response['content'])
    except Exception as exception:
        log('handle_response Error: ', exception)
        return

def get_voice():
    if (useVoice):
        try: 
            # use the microphone as source for input. 
            with sr.Microphone() as source2: 
                
                log("Info: Say something")
                # wait for a second to let the recognizer 
                # adjust the energy threshold based on 
                # the surrounding noise level  
                r.adjust_for_ambient_noise(source2, duration=0.2) 
                
                #listens for the user's input  
                audio2 = r.listen(source2) 
                
                # Using ggogle to recognize audio 
                voiceText = r.recognize_google(audio2) 
                voiceText = voiceText.lower() 
    
                log("Info: You said = " + voiceText) 

                return voiceText
              
        except sr.RequestError as e: 
            log("get_voice Error: Could not request results; {0}".format(e)) 
            return ''
            
        except sr.UnknownValueError: 
            log("get_voice Recognition Error: Unknown error") 
            return ''
    else:
        userInput = input('Input command: ')
        log("Input command: ", userInput)
        return userInput

class RunTaskServer(threading.Thread):

    def run(self):
        global task_socket
        
        task_socket.connect((HOST, PORT))  # connect to the server

        config.setup()
        voice.setup()

        # initial handshake
        response = send_task_socket('handshake', '', True)

        # WAITING FOR VOICE INPUT
        message = get_voice()

        success, pro, struct = input_control.Process(message)

        while message.lower().strip() != 'unicorn':
            if (success):
                response = send_task_socket('message', { 'pro': pro, 'struct': struct }, True)

                handle_response(response)

            # WAITING FOR VOICE INPUT
            message = get_voice()

            success, pro, struct = input_control.Process(message)


if (__name__ == '__main__'):
    task_socket = socket.socket()  # instantiate
    info_socket = socket.socket()  # instantiate
 
    try:
        task_server_thread = RunTaskServer(name = "Task-Server")
        task_server_thread.start()

        info_socket.connect((HOST, INFO_PORT))  # connect to the server

        print ("New Device ID: ", device_key)
    except KeyboardInterrupt:
        task_socket.close()
        info_socket.close()
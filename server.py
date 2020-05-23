#!/usr/bin/env python3
from helper import tasks
from Naked.toolshed.shell import execute_js, muterun_js
from subprocess import check_output

import os
import array
import sys
import socketserver
import socket
import json
import config
import asyncio
import websockets

import threading
import time

import asyncore
import logging

import admin_manager

global server
global info_server

device = admin_manager.get_device_type()

HOST = admin_manager.get_ip(device)
PORT = 65432
INFO_PORT = 65433
NOTIF_PORT = 65434
WEB_PORT = 8765

open_connections = []

#ID: False / True (based on if they're online)
active_clients = {}
heart_beat_timeout = 5 #seconds

MASTER_STOP = False

print("========================================")
print("DEVICE IP: ", HOST)
print("DEVICE: ", device)
print("========================================")

def setup():
    config.setup()

    active_clients["server"] = {
        "version": config.CONFIG["version"]
    }

def handle_input(address, json_content):
    global active_clients
    
    sendToAll = False
    respond = False
    type = ''
    stringMessage = ''

    clientID = json_content['ID']
    messageType = json_content['type']
    clientLogger = json_content['logger']
    
    if (messageType == 'handshake'):
        print("CONNECTION: ", clientID)
        active_clients[clientID] = { 'active': True, 'logger': clientLogger, 'address': address }
        respond = True
        type = 'handshake'

    elif (messageType == 'disconnection'):
        print("DISCONNECTION: ", clientID)
        active_clients[clientID]['active'] = False

    elif (messageType == 'message'):
        respond = True
        type = "voice_response"
        stringMessage = tasks.ProcessTask(input, json_content['content']["pro"], json_content['content']["struct"])

    active_clients[clientID]['logger'] = clientLogger
    
    return (sendToAll, respond, type, stringMessage)

def create_response(type, content):
    return json.dumps({
        'ID': 'MOTHER-SHIP',
        'type': type,
        'content': content
    })

def send_to_all(message):
    for client in open_connections:
        client.handle_write(message)

def read_socket_request(data):
    json_data = json.loads(data)

    if (json_data['type'] == 'get-info'):
        return create_response('data_response', active_clients)
    if (json_data['type'] == 'update-sandra'):

        message = create_response("update", "").encode('utf-8')

        send_to_all(message)

        if (device == 'Pi'):
            resposne = admin_manager.update_system(config.CONFIG['version'])
            print(response)
        
    return ('error')

# Main tasks server
class Server(asyncore.dispatcher):
    def __init__(self, address):
        asyncore.dispatcher.__init__(self)
        self.logger = logging.getLogger('TASK_SERVER')
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(address)
        self.address = self.socket.getsockname()
        self.logger.debug('binding to %s', self.address)
        self.listen(5)

    def handle_accept(self):
        # Called when a client connects to our socket
        client_info = self.accept()
        if client_info is not None:
            self.logger.debug('handle_accept() -> %s', client_info[1])
            ClientHandler(client_info[0], client_info[1])

    def stop(self):
        self.stop()
        self.close()

class ClientHandler(asyncore.dispatcher):
    id = ''
    device_address = ''

    def __init__(self, sock, address):
        global device_address
        device_address = address
        asyncore.dispatcher.__init__(self, sock)
        self.logger = logging.getLogger('Client ' + str(address))
        self.data_to_write = []

    def writable(self):
        return bool(self.data_to_write)

    def handle_write(self, to_send):
        sent = self.send(to_send)
        
        self.logger.debug('handle_write() -> (%d) "%s"', sent, "SUCCESS")

    def handle_read(self):
        data = self.recv(1024).decode('utf-8')
        
        # If client disconnects due to error
        if (not data):
            self.handle_close()
            print("CLIENT ERROR: Close client")
            return

        self.logger.debug('handle_read() -> (%d) "%s"', len(data), data.rstrip())

        #try:
        recieved = json.loads(data)

        sendToAll, should_respond, type, stringMessage = handle_input(device_address, recieved)

        if (recieved['type'] == 'handshake'):
            self.id = recieved['ID']

        if (should_respond):
            # Creating json response and stringifying it
            to_send = create_response(type, stringMessage).encode('utf-8')

            if (sendToAll):
                self.handle_write(to_send)
            else: 
                print("sent response")
                self.handle_write(to_send)
        else:
            self.handle_write(json.dumps({type: 'validation', stringMessage: "success"}).encode('utf-8'))


    def handle_close(self):
        active_clients[self.id]['active'] = False
        print(active_clients)
        self.logger.debug('handle_close()')
        self.close()

class Socket_Server(threading.Thread):
    def run(self):
        global server
        logging.basicConfig(level=logging.DEBUG, format='%(name)s:[%(levelname)s]: %(message)s')
        server = Server((HOST,PORT))    
        asyncore.loop()

# Main tasks server
class NotifServer(asyncore.dispatcher):
    def __init__(self, address):
        asyncore.dispatcher.__init__(self)
        self.logger = logging.getLogger('NOTIFICATION_SERVER')
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(address)
        self.address = self.socket.getsockname()
        self.logger.debug('binding to %s', self.address)
        self.listen(5)

    def handle_accept(self):
        # Called when a client connects to our socket
        client_info = self.accept()
        if client_info is not None:
            self.logger.debug('handle_accept() -> %s', client_info[1])
            newClient = NotifClientHandler(client_info[0], client_info[1])
            open_connections.append(newClient)

    def stop(self):
        self.stop()
        self.close()

class NotifClientHandler(asyncore.dispatcher):
    id = ''
    device_address = ''

    def __init__(self, sock, address):
        global device_address
        device_address = address
        asyncore.dispatcher.__init__(self, sock)
        self.logger = logging.getLogger('Client ' + str(address))
        self.data_to_write = []

    def writable(self):
        return bool(self.data_to_write)

    def handle_write(self, to_send):
        sent = self.send(to_send)
        
        self.logger.debug('handle_write() -> (%d) "%s"', sent, "SUCCESS")

    def handle_close(self):
        self.logger.debug('handle_close()')
        self.close()

class Notif_Socket_Server(threading.Thread):
    def run(self):
        global server
        logging.basicConfig(level=logging.DEBUG, format='%(name)s:[%(levelname)s]: %(message)s')
        server = NotifServer((HOST,NOTIF_PORT))    
        asyncore.loop()

# Main web dashboard
class Web_Server(threading.Thread):
    def run(self):
        print("Starting up webserver")
        result = execute_js('./website/server.js')
        if result:
            print("Done website")
            # JavaScript is successfully executed
        else:
            print("failed")
            # JavaScript is failed

async def listen(websocket, path):
    async for message in websocket:
        
        response = read_socket_request(message)

        await websocket.send(response)

class WebSocket_Server(threading.Thread):

    def run(self):
        print("starting")
        asyncio.set_event_loop(asyncio.new_event_loop())
        asyncio.get_event_loop().run_until_complete( websockets.serve(listen, HOST, WEB_PORT) )
        asyncio.get_event_loop().run_forever()

        print("finished")

# Information updater from client
class Info_Server(asyncore.dispatcher):
    def __init__(self, address):
        asyncore.dispatcher.__init__(self)
        self.logger = logging.getLogger('INFO_SERVER:')
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(address)
        self.address = self.socket.getsockname()
        self.logger.debug('binding to %s', self.address)
        self.listen(5)

    def handle_accept(self):
        # Called when a client connects to our socket
        client_info = self.accept()
        if client_info is not None:
            self.logger.debug('handle_accept() -> %s', client_info[1])
            InfoClientHandler(client_info[0], client_info[1])

    def stop(self):
        self.stop()
        self.close()

class InfoClientHandler(asyncore.dispatcher):
    id = ''
    device_address = ''

    def __init__(self, sock, address):
        global device_address
        device_address = address
        
        asyncore.dispatcher.__init__(self, sock)
        self.logger = logging.getLogger('Client ' + str(address))
        self.data_to_write = []

    def writable(self):
        return bool(self.data_to_write)

    def handle_write(self, to_send):
        sent = self.send(to_send)
        self.logger.debug('handle_write() -> (%d) "%s"', sent, "SUCCESS")

    def handle_read(self):
        data = self.recv(1024).decode('utf-8')

        # If client disconnects due to error
        if (not data):
            self.handle_close()
            print("CLIENT ERROR: Close client")
            return

        self.logger.debug('handle_read() -> (%d) "%s"', len(data), data.rstrip())

        #try:
        recieved = json.loads(data)

        active_clients[recieved['ID']]['logger'] = recieved['logger']

        self.handle_write(json.dumps({'type': 'validation', 'response': 'success'}).encode('utf-8'))

    def handle_close(self):
        self.close()

class Information_Server(threading.Thread):
    def run(self):
        global info_server
        logging.basicConfig(level=logging.DEBUG, format='%(name)s:[%(levelname)s]: %(message)s')
        info_server = Info_Server((HOST,INFO_PORT))    
        asyncore.loop()

def start():
    setup()

    CLOSE_PROGRAM = False

    try:
        mythread = Socket_Server(name = "Socket-Server") 
        mythread.setDaemon(True)
        mythread.start()

        info_server_thread = Information_Server(name = "Information-Server") 
        info_server_thread.setDaemon(True)
        info_server_thread.start()

        web_socket_thread = WebSocket_Server(name = "WebSocket-Server") 
        web_socket_thread.setDaemon(True)
        web_socket_thread.start()

        notif_server_thread = Notif_Socket_Server(name = "Notification-Server") 
        notif_server_thread.setDaemon(True)
        notif_server_thread.start()

        web_server_thread = Web_Server(name = "Website-Server") 
        web_server_thread.setDaemon(True)
        web_server_thread.start()
        
        while not CLOSE_PROGRAM:
            if (CLOSE_PROGRAM):
                break

    except KeyboardInterrupt:
        CLOSE_PROGRAM = True
        server.close()
        info_server.close()
        exit()
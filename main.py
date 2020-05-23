import socket
import server
import client
import sys

arg = False

if (len(sys.argv) > 1):
    if (sys.argv[1] == 'debug_server'):
        server.start()

device_name = socket.gethostname()

if (device_name == "SANDRA_Server"):
    server.start()
else:
    client.start()
import socket
import sys
import config

config.setup()

if (len(sys.argv) > 1):
    print(sys.argv[1])
    if (sys.argv[1] == 'debug_server'):
        import server
else :
    device_name = socket.gethostname()

    if (device_name == "SANDRA_Server"):
        import server
    else:
        import client
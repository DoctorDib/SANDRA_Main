import os
import socket

def get_device_type():
    if (os.name == 'nt'):
        return 'Windows'
    else:
        from subprocess import check_output
        return 'Pi'

def get_ip(type):
    if (type == 'Windows'):
        return socket.gethostbyname(socket.gethostname())
    else:
        from subprocess import check_output
        return str(check_output(['hostname', '-I'])).split('\'')[1].split(' ')[0]

def update_system():
    os.system('git pull')
    reboot()

def shutdown():
    os.system('sudo shutdown -h now')

def reboot():
    os.system('sudo reboot')
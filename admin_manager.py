import os
import socket
import config

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

def update_system(currentVerison):
    os.system('git pull')

    config.setup()
    newVersion = config.CONFIG['version']

    # Ensure that version is up to speed
    if (newVersion != currentVerison):
        reboot()
    else:
        return "Already updated to the latest version"

def shutdown():
    os.system('sudo shutdown -h now')

def reboot():
    os.system('sudo reboot')
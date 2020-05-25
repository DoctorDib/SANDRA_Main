from datetime import datetime
import platform
import subprocess

VOLTAGE_MESSAGE = {
    0: 'Under-voltage!',
    1: 'ARM frequency capped!',
    2: 'Currently throttled!',
    3: 'Soft temperature limit active',
    16: 'Under-voltage has occurred since last reboot.',
    17: 'Throttling has occurred since last reboot.',
    18: 'ARM frequency capped has occurred since last reboot.',
    19: 'Soft temperature limit has occurred'
}

def run_command(command):
    response = ""

    try:
        response =  subprocess.check_output("vcgencmd ", command, shell=True)
    except Exception as error:
        print(error)

        response = "Error"
    finally:
        return response

def get_throttled():
    response = run_command("get_throttled")

    if (response == "Error"):
        return response

    print(">>", response)

    throttled_binary = bin(int(run_command("get_throttled").split('=')[1], 0))

    warnings = 0
    message = ""
    for position, message in VOLTAGE_MESSAGE.iteritems():
        # Check for the binary digits to be "on" for each warning message
        if len(throttled_binary) > position and throttled_binary[0 - position - 1] == '1':
            print(message)
            warnings += 1

    return dict(cpu_core_frequency=message)


throttle = get_throttled()

print(throttle)
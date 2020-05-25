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

    command = "vcgencmd " + command

    try:
        response =  subprocess.check_output(command, shell=True)
        response = response.split('=')[1].split('\\n')[0]
    except Exception as error:
        print(error)

        response = "Error"
    finally:
        return response

def get_throttled():
    response = run_command("get_throttled")

    if (response == "Error"):
        return response

    throttled = int(run_command("get_throttled"), 16)

    throttling_occurred = (throttled & 0x40000) >> 18
    arm_frequency_capped_occurred = (throttled & 0x20000) >> 17
    under_voltage_occurred = (throttled & 0x10000) >> 16
    currently_throttled = (throttled & 0x4) >> 2
    arm_frequency_capped = (throttled & 0x2) >> 1
    under_voltage = (throttled & 0x1)

    results = {
        'throttling_occurred': throttling_occurred,
        'arm_frequency_capped_occurred': arm_frequency_capped_occurred,
        'under_voltage_occurred': under_voltage_occurred,
        'currently_throttled': currently_throttled,
        'arm_frequency_capped': arm_frequency_capped,
        'under_voltage': under_voltage,
    }

    print(results)

    return dict(cpu_core_frequency=results)


throttle = get_throttled()

print(throttle)
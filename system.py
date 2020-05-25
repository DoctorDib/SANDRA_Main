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
        response = str(response).split('=')[1].split('\\n')[0]
    except Exception as error:
        print(error)
        response = "Error"
    finally:
        return response

def get_power_condition():
     results = []

    throttled = int(run_command("get_throttled"), 16)

    if (response == "Error"):
        return response

    # SOLUTION
    #https://gist.github.com/fernandog/d330f87b19c2ace350110cb697504fc2

    if ((throttled & 0x40000) >> 18):
        results.append("throttling_occurred")

    if ((throttled & 0x20000) >> 17):
        results.append("arm_frequency_capped_occurred")

    if ((throttled & 0x10000) >> 16):
        results.append("under_voltage_occurred")

    if ((throttled & 0x4) >> 2):
        results.append("currently_throttled")

    if ((throttled & 0x2) >> 1):
        results.append("arm_frequency_capped")

    if ((throttled & 0x1)):
        results.append("under_voltage")

    print(results)

    return dict(cpu_core_frequency=results)

def get_measure():
    temp = run_command("measure_temp")

throttle = get_power_condition()
print(throttle)

temperature = get_measure()
print(temperature)
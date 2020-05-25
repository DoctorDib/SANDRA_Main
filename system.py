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

# TASKS

def get_power_condition():
    results = []

    throttled = int(run_command("get_throttled"), 16)

    if (throttled == "Error"):
        return throttled

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

    return results

def get_measure():
    # Getting current temp of pi
    return run_command("measure_temp")

def get_volts():
    # Getting current volts of pi
    return run_command("measure_volts core")

def get_mem(type):
    return run_command("get_mem " + type)

def get_number_of_oom():
    # Getting number of out of memory events
    return run_command("mem_oom")

def get_hertz(type):
    hertz = run_command("measure_clock " + type)

    return (hertz * 0.000001) + " MHz"

## INPUTS
throttle = get_power_condition()
print(throttle)

temperature = get_measure()
print(temperature)

memory_of_arm = get_mem("arm")
print("Memory of arm: ", memory_of_arm)

memory_of_gpu = get_mem("gpu")
print("Memory of GPU: ", memory_of_gpu)

# Graphics 
arm_hert = get_hertz("arm")
print("ARM: ", arm_hert)

# Core
core_hert = get_hertz("core")
print("Core: ", core_hert)

# Audio
pwm_hert = get_hertz("pwm")
print("Audio: ", pwm_hert)

# SD
emmc_hert = get_hertz("emmc")
print("SD: ", emmc_hert)
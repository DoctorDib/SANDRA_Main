from datetime import datetime
import platform
import subprocess

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
    throttled = int(run_command("get_throttled"), 16)

    if (throttled == "Error"):
        return throttled

    # SOLUTION
    #https://gist.github.com/fernandog/d330f87b19c2ace350110cb697504fc2

    return {
        "throttling_occurred": (throttled & 0x40000) >> 18,
        "arm_frequency_capped_occurred": (throttled & 0x20000) >> 17,
        "under_voltage_occurred": (throttled & 0x10000) >> 16,
        "currently_throttled": (throttled & 0x4) >> 2,
        "arm_frequency_capped": (throttled & 0x2) >> 1,
        "under_voltage": (throttled & 0x1)
    }

def get_temperature():
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

    return float(hertz) * 0.000001


# Getting the specs
def get_system_specs():
    return {
        "power_condition": get_power_condition(),
        "temperature": get_temperature(),
        "memory": {
            "arm": get_mem("arm"),
            "gpu": get_mem("gpu")
        },
        "mherz": {
            "arm": get_hertz("arm"),
            "core": get_hertz("core"),
            "pwm": get_hertz("pwn"),
            "emmc": get_hertz("emmc")
        }
    }
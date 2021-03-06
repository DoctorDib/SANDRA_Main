from datetime import datetime
from subprocess import check_output
from re import findall
import platform
import psutil
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

def bytes_to_megabytes(inputDict):
    for key in inputDict:
        # Skipping percentage
        if (key == "percent"):
            inputDict[key] = float(inputDict[key])
            continue

        # "%.2f" rounding to two decimal places
        inputDict[key] = float("%.2f" % (float(inputDict[key]) * 0.000001))

    return inputDict

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

def get_temp():
    temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
    return(findall("\d+\.\d+",temp)[0])

def get_disk_usage():
    results = psutil.disk_usage('/')
    results = {
        "total": results.total,
        "used": results.used,
        "free": results.free,
        "percent": results.percent
    }

    return bytes_to_megabytes(results)

def get_memory_usage():
    results = psutil.virtual_memory()
    results = {
        "total": results.total,
        "available": results.available,
        "percent": results.percent,
        "used": results.used,
        "free": results.free,
        "active": results.active,
        "inactive": results.inactive,
        "buffers": results.buffers,
        "cached": results.cached,
        "shared": results.shared,
    }
    return bytes_to_megabytes(results)

def get_swap_memory_usage():
    results = psutil.swap_memory()
    results = {
        "total": results.total,
        "used": results.used,
        "free": results.free,
        "percent": results.percent,
        "sin": results.sin,
        "sout": results.sout
    }

    return bytes_to_megabytes(results)

def get_cpu_usage():
    return str(psutil.cpu_percent(interval=None))

# Getting the specs
def get_system_specs():
    return {
        "power_condition": get_power_condition(),
        "temperature": get_temp(),
        "disk_usage": get_disk_usage(),
        "memory_usage": get_memory_usage(),
        "swap_memory_usage": get_swap_memory_usage(),
        "cpu_usage": get_cpu_usage()    
    }
    
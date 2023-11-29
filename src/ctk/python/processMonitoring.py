from typing import Union
from datetime import datetime
import time
import psutil


def check_process_exists(process_name):
    for process in psutil.process_iter(['pid', 'name']):
        # print(process)
        if process.info['name'] == process_name:
            return True
    return False


def get_duration_until_process_started(process_name, monitoring_duration_sec):
    monitoring_start_time = datetime.now()
    print("monitoring_start_time", monitoring_start_time)

    while (datetime.now() - monitoring_start_time).total_seconds() < monitoring_duration_sec:
        if check_process_exists(process_name):
            duration_until_process_started = datetime.now() - monitoring_start_time
            print(f"The process '{process_name}' exists. It took {duration_until_process_started} to restart.")
            return duration_until_process_started  # Exit the loop if the process is found

        # Wait for a short interval before checking again
        time.sleep(1)

    else:
        print(f"The process '{process_name}' was not found within {monitoring_duration_sec} seconds.")
        return None


get_duration_until_process_started("KeePassXC.exe", 5)

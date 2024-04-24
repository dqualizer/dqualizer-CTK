import os
import subprocess
import time

import psutil

import processStarting

# This simulates an fallback mechanism, which automatically watches a process and restarts if it is not present anymore
# As this should be implemented externally, by companys themselves, hardcoded path is okay here
# THIS NOT INTENDED TO BE USED BY CTK EXPERIMENTS

process_name = "leasingninja-riskApi-0.0.1"
process_path = "C:\\Users\\HenningMöllers\\IdeaProjects\\leasing-ninja\\leasingninja-riskApi\\target\\leasingninja-riskApi-0.0.1-SNAPSHOT.jar"

while True:
    # Get PID, in case searched processes runs in JVM, as they just have the name 'java' in os
    # initialize with negative PID, as its definitely not found in system processes
    pid_for_searched_jvm_process = -1
    os.environ['PATH'] = "C:\\Users\\HenningMöllers\\.jdks\\openjdk-21.0.2\\bin"
    jps_processes = subprocess.check_output(["jps"]).decode("utf-8").split("\n")

    for line in jps_processes:
        if process_name in line:
            line = line.split()
            pid_for_searched_jvm_process = line[0]
            break

    process_active = False
    for proc in psutil.process_iter():
        # Check for process name or the eventually defined process id
        if proc.name() == process_name or proc.pid == int(pid_for_searched_jvm_process):
            #print(f"Found process '{proc}'. Restarting not necessary")
            process_active = True

    if not process_active:
        time.sleep(1.5)
        processStarting.start_java_process_by_path(1, 2, 3, 4, process_path, 5)
        print(f"Process '{process_name}' NOT found. Restarted it.")

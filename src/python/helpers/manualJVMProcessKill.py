import os
import subprocess
import psutil

# This script is intended to be used to MANUALLY kill a JVM by the process name
# This script is NOT intended to be used by CTK experiments.

process_name = "leasingninja-riskApi-0.0.1"

pid_for_searched_jvm_process = -1
os.environ['PATH'] = "C:\\Users\\HenningMöllers\\.jdks\\openjdk-21.0.2\\bin"
jps_processes = subprocess.check_output(["jps"]).decode("utf-8").split("\n")

for line in jps_processes:
    if process_name in line:
        line = line.split()
        pid_for_searched_jvm_process = line[0]
        break

for proc in psutil.process_iter():
    # Check for process name or the eventually defined process id
    if proc.name() == process_name or proc.pid == int(pid_for_searched_jvm_process):
        print(f"Kill process: '{proc}'")
        # Do SIGTerm to stop process gracefully, replace with proc.kill() to stop the process forcefully
        proc.kill()

import subprocess
import psutil
import mySqlConnector
import os


# Kill a process cross-platform
def kill_process_by_name(db_username, db_password, username, password, process_name):
    connection = mySqlConnector.create_db_connection(db_username, db_password)
    authenticated = mySqlConnector.authenticate_user(connection, username, password)

    if authenticated:
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

        for proc in psutil.process_iter():
            # Check for process name or the eventually defined process id
            if proc.name() == process_name or proc.pid == int(pid_for_searched_jvm_process):
                print(f"Kill process: '{proc}'")
                # Do SIGTerm to stop process gracefully, replace with proc.kill() to stop the process forcefully
                proc.kill()

                return True

        print(f"Process to kill '{proc}' was not found found.")
        return False

    else:
        print(f"Failed to authenticate")
        return False

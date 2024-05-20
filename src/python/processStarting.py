import subprocess
import os

import mySqlConnector


def start_process_by_path(db_username, db_password, username, password, path, log_result_in_influx_db):
    print(f"Please start process at {path} manually.")
    # subprocess.Popen([path], shell=True)


def start_jvm_process_by_path(db_username, db_password, username, password, path):
    connection = mySqlConnector.create_db_connection(db_username, db_password)
    authenticated = mySqlConnector.authenticate_user(connection, username, password)

    if authenticated:
        os.environ['PATH'] = "C:\\Users\\HenningMöllers\\.jdks\\openjdk-21.0.2\\bin"
        started_process_pid = subprocess.Popen(["java", "-jar", path]).pid
        print(f"Started process has PID: {started_process_pid}")

    # TODO use Exception from chaostoolkit library if available
    else:
        print(f"Failed to authenticate")
        return False

# start_process_by_path(r"C:\Program Files\KeePassXC\KeePassXC.exe")

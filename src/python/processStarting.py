import subprocess
import os

import mySqlConnector
import influxDBConnector

def start_process_by_path(db_username, db_password, username, password, path, log_result_in_influx_db):
    print(f"Please start process at {path} manually.")
    # subprocess.Popen([path], shell=True)


def start_jvm_process_by_path(db_username, db_password, username, password, path, process_name):
    connection = mySqlConnector.create_db_connection(db_username, db_password)
    authenticated = mySqlConnector.authenticate_user(connection, username, password)

    if authenticated:
        # Retrieve the JAVA_HOME environment variable
        java_home = os.environ.get('JAVA_HOME')
        os.environ['PATH'] = java_home + "\\bin"
        started_process_pid = subprocess.Popen(["java", "-jar", path]).pid
        print(f"Started process has PID: {started_process_pid}")
        influxDBConnector.write_monitoring_data("process_running", "process_name", process_name, "is_running",
                                                True)

    # TODO use Exception from chaostoolkit library if available
    else:
        print(f"Failed to authenticate")
        return False

# start_process_by_path(r"C:\Program Files\KeePassXC\KeePassXC.exe")

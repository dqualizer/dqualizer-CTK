import subprocess
from datetime import datetime
import time
import psutil
import influxDBConnector
import mySqlConnector
import os


def check_process_exists(db_username, db_password, username, password, process_name, log_result_in_influx_db):
    connection = mySqlConnector.create_db_connection(db_username, db_password)
    authenticated = mySqlConnector.authenticate_user(connection, username, password)

    if authenticated:

        print("checking " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        # check non-jvm processes for matching process name
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == process_name:
                if log_result_in_influx_db:
                    influxDBConnector.write_monitoring_data("process_running", "process_name", process_name, "is_running",
                                                            True)
                print('Process exists!')
                return True

        # check jvm processes for matching process name
        # Retrieve the JAVA_HOME environment variable
        java_home = os.environ.get('JAVA_HOME')
        os.environ['PATH'] = java_home + "\\bin"
        jps_processes = subprocess.check_output(["jps"]).decode("utf-8").split("\n")
        for line in jps_processes:
            if process_name in line:
                influxDBConnector.write_monitoring_data("process_running", "process_name", process_name, "is_running",
                                                        True)
                print('Process exists!')

                return True

        if log_result_in_influx_db:
            influxDBConnector.write_monitoring_data("process_running", "process_name", process_name, "is_running", False)

        print('Process does NOT exist!')
        return False

    # TODO use Exception from chaostoolkit library if available
    else:
        print(f"Failed to authenticate")
        return False


def get_duration_until_process_started(db_username, db_password, username, password, process_name, monitoring_duration_sec, checking_interval_sec):
    # We assume that the process is already terminated
    monitoring_start_time = datetime.now()
    # print("monitoring_start_time", monitoring_start_time)

    while (datetime.now() - monitoring_start_time).total_seconds() < monitoring_duration_sec:
        if check_process_exists(db_username, db_password, username, password, process_name, True):
            duration_until_process_started_milliseconds = datetime.now().timestamp()*1000 - monitoring_start_time.timestamp()*1000
            print(f"The process '{process_name}' exists. It took {duration_until_process_started_milliseconds} milliseconds to restart.")
            influxDBConnector.write_monitoring_data("actual_response_measure", "",
                                                    "",
                                                    'actual_recovery_time',
                                                    duration_until_process_started_milliseconds)
            return duration_until_process_started_milliseconds

        # Wait for a short interval before checking again
        # Is currently technically limited to precision of max. 1-2 checks per second
        time.sleep(checking_interval_sec)

    else:
        print(f"The process '{process_name}' was not found within {monitoring_duration_sec} seconds.")
        influxDBConnector.write_monitoring_data("actual_response_measure", "",
                                                "",
                                                'actual_recovery_time', -1)
        return None


# get_duration_until_process_started("KeePassXC.exe", 5, 0)

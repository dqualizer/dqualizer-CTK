import subprocess


# Alternativ mit import os, os.system(command) aber nicht empfohlen

def start_process_by_path(db_username, db_password, username, password, path, log_result_in_influx_db):
    print(f"Please start process at {path} manually.")
    #subprocess.Popen([path], shell=True)

# TODO JAVA Process starten subprocess.Popen([java_command, "-jar", jar_file]
# Backslashes werden in Python escaped
# start_process_by_path(r"C:\Program Files\KeePassXC\KeePassXC.exe")

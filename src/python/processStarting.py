import subprocess


# Alternativ mit import os, os.system(command) aber nicht empfohlen

def start_process_by_path(path):
    print(f"Please start process at {path} manually.")
    #subprocess.Popen([path], shell=True)


# Backslashes werden in Python escaped
# start_process_by_path(r"C:\Program Files\KeePassXC\KeePassXC.exe")

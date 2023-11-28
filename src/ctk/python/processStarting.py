import subprocess


# Alternativ mit import os, os.system(command) aber nicht empfohlen

def start_process_by_path(path):
    print(path)
    command = 'Start-Process -FilePath \'' + path + '\''
    print(command)
    subprocess.run([command], shell=True)


# Backslashes werden in Python escaped
start_process_by_path("C:\\Program Files\\KeePassXC\\KeePassXC.exe")
## TODO Funktioniert, ChatGPT fragen
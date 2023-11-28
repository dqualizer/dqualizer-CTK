import psutil


# Kill process cross platform
def kill_process_by_name(process_name):
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == process_name:
            print(f"Kill process: '{proc}'")
            proc.kill()


kill_process_by_name("KeePassXC.exe")

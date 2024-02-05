import psutil
import mySqlConnector


# Kill process cross platform
def kill_process_by_name(db_username, db_password, username, password, process_name):

    connection = mySqlConnector.create_db_connection(db_username, db_password)
    authenticated = mySqlConnector.authenticate_user(connection, username, password)

    if authenticated:
        for proc in psutil.process_iter():
            # Check whether the process name matches
            if proc.name() == process_name:
                print(f"Kill process: '{proc}'")
                # do SIGKill to stop process gracefully
                proc.kill()
                return True

        print(f"Process to kill '{proc}' was not found found.")
        return False

    else:
        print(f"Failed to authenticate")
        return False



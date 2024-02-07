import hashlib
import sys
import mysql.connector
import config


def create_db_connection(mysql_username, mysql_password):
    mysql_config = config.db_base_config
    mysql_config['user'] = mysql_username
    mysql_config['password'] = mysql_password

    try:
        connection = mysql.connector.connect(**mysql_config)
        if connection.is_connected():
            # print(f"Connected to MySQL database: {mysql_config['database']}")
            return connection

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def authenticate_user(connection, username, password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))

    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM users WHERE username = %s AND password_hash = %s"
    cursor.execute(query, (username, sha256.hexdigest()))

    result = cursor.fetchone()
    cursor.close()

    authenticated = result[0] > 0
    return authenticated

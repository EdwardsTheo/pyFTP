import sqlite3

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('C:\\Users\\bapti\\Desktop\\SRC_FTP-master\\SQL\\ftpServer.db')
    except Error as e:
        print(e)

    return conn
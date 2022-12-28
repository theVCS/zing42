from mysql import connector

def connect():
    return connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database='zing42'
    )

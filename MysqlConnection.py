# bin/detect
from mysql.connector import connect, errorcode, Error


def connect_mysql():
    try:
        database_connect = connect(host="localhost", user="root", password="Pwd$4mysql520", database="pizza")
        return database_connect
    except Error as er:
        if er.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password!")
            return False
        elif er.errno == errorcode.ER_BAD_DB_ERROR:
            print("No such databases exist!")
            return False
        else:
            print(er)
            return False



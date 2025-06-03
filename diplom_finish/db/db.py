import pymysql
from pymysql import cursors

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="diplom",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
        port=3312
    )

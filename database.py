import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  
    'database': 'smartwatcher_ai'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)
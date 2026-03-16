import mysql.connector

def get_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword",
        database="quantumfinance"
    )
    return conn

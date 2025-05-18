import mysql.connector
from mysql.connector import Error

def stream_users():
    """Generator function that streams rows from user_data table one by one"""
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev'
        )
        
        cursor = connection.cursor(dictionary=True)
        
        # Execute the query
        cursor.execute("SELECT * FROM user_data")
        
        # Stream rows one by one using yield
        row = cursor.fetchone()
        while row is not None:
            yield row
            row = cursor.fetchone()
            
    except Error as e:
        print(f"Database error: {e}")
    finally:
        # Clean up resources
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

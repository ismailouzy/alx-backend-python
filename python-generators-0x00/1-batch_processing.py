import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """Generator function that streams rows from user_data table in batches"""
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
        
        # Stream rows in batches
        while True:
            batch = []
            for _ in range(batch_size):
                row = cursor.fetchone()
                if row is None:
                    break
                batch.append(row)
            
            if not batch:
                break
                
            yield batch
            
    except Error as e:
        print(f"Database error: {e}", file=sys.stderr)
    finally:
        # Clean up resources
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

def batch_processing(batch_size):
    """Processes batches of users and filters those over age 25"""
    for batch in stream_users_in_batches(batch_size):
        # Filter users over 25
        filtered_users = [user for user in batch if user['age'] > 25]
        
        # Yield each filtered user one by one
        for user in filtered_users:
            yield user

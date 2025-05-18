import mysql.connector
from mysql.connector import Error

def stream_user_ages():
    """Generator function that streams user ages one by one"""
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev'
        )
        
        cursor = connection.cursor()
        
        # Execute the query to get only ages
        cursor.execute("SELECT age FROM user_data")
        
        # Stream ages one by one using yield
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row[0]
            
    except Error as e:
        print(f"Database error: {e}")
    finally:
        # Clean up resources
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

def calculate_average_age():
    """Calculates the average age using the streamed ages"""
    total = 0
    count = 0
    
    # Single loop to process all ages
    for age in stream_user_ages():
        total += age
        count += 1
    
    # Calculate average if we have data
    if count > 0:
        average = total / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users found in the database")

if __name__ == "__main__":
    calculate_average_age()

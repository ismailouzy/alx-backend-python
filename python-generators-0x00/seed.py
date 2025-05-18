import mysql.connector
from mysql.connector import Error
import uuid
import csv
import os

def connect_db():
    """Connect to the MySQL database server"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_database(connection):
    """Create the database ALX_prodev if it does not exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created successfully")
    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        if cursor:
            cursor.close()

def connect_to_prodev():
    """Connect to the ALX_prodev database in MySQL"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev'
        )
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None

def create_table(connection):
    """Create the table user_data if it does not exist with the required fields"""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(10,0) NOT NULL,
        INDEX (user_id)
    )
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        if cursor:
            cursor.close()

def insert_data(connection, csv_file):
    """Insert data from CSV file into the database if it does not exist"""
    if not os.path.exists(csv_file):
        print(f"CSV file {csv_file} not found")
        return

    try:
        cursor = connection.cursor()
        
        # Check if table is empty
        cursor.execute("SELECT COUNT(*) FROM user_data")
        count = cursor.fetchone()[0]
        if count > 0:
            print("Data already exists in the table")
            return

        with open(csv_file, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Generate UUID if not present in csv
                user_id = row.get('user_id', str(uuid.uuid4()))
                name = row['name']
                email = row['email']
                age = row['age']
                
                # Check if record already exists
                cursor.execute(
                    "SELECT user_id FROM user_data WHERE user_id = %s",
                    (user_id,)
                )
                if cursor.fetchone() is None:
                    cursor.execute(
                        "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                        (user_id, name, email, age)
                    )
        
        connection.commit()
        print("Data inserted successfully")
    except Error as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
    finally:
        if cursor:
            cursor.close()

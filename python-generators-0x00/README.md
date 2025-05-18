# MySQL Database Seeder for ALX_prodev

This Python script sets up a MySQL database named `ALX_prodev` with a `user_data` table and populates it with data from a CSV file.

## Features

- Creates the `ALX_prodev` database if it doesn't exist
- Creates a `user_data` table with the following schema:
  - `user_id` (Primary Key, UUID, Indexed)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)
- Populates the table with data from a CSV file
- Prevents duplicate entries

## Prerequisites

- Python 3.x
- MySQL server installed and running
- Python packages:
  - `mysql-connector-python`
  - `uuid`
  - `csv`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/alx-backend-python.git
   cd alx-backend-python/python-generators-0x00
   ```

2. Install the required packages:
   ```bash
   pip install mysql-connector-python
   ```

## Configuration

By default, the script uses the following MySQL credentials:
- Host: `localhost`
- User: `root`
- Password: `''` (empty string)
- Database: `ALX_prodev`

If you need to change these, modify the connection parameters in the `connect_db()` and `connect_to_prodev()` functions in `seed.py`.

## Usage

1. Prepare your CSV file (`user_data.csv`) with the following columns:
   - `user_id` (optional - will be auto-generated if missing)
   - `name` (required)
   - `email` (required)
   - `age` (required)

2. Run the script:
   ```bash
   python3 0-main.py
   ```

## Expected Output

Successful execution will show:
```
connection successful
Database ALX_prodev created successfully
Table user_data created successfully
Data inserted successfully
Database ALX_prodev is present 
[Sample rows from the database]
```

## Functions Overview

1. `connect_db()` - Connects to the MySQL server
2. `create_database(connection)` - Creates the ALX_prodev database
3. `connect_to_prodev()` - Connects to the ALX_prodev database
4. `create_table(connection)` - Creates the user_data table
5. `insert_data(connection, data)` - Inserts data from CSV file

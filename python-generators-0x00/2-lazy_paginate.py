import sys
from seed import connect_to_prodev

def paginate_users(page_size, offset):
    """Fetch a page of users from the database"""
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

def lazy_paginate(page_size):
    """Generator function that lazily paginates through users"""
    offset = 0
    while True:
        # Fetch the next page
        page = paginate_users(page_size, offset)
        
        # If page is empty, we're done
        if not page:
            break
        
        # Yield the current page
        yield page
        
        # Update offset for next iteration
        offset += page_size

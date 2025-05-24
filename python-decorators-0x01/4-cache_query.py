import time
import sqlite3
import functools
from functools import wraps

query_cache = {}

def cache_query(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from kwargs or args
        query = kwargs.get('query', None)
        if query is None and len(args) > 1:  # args[0] is conn, args[1] is query
            query = args[1]
        
        if query not in query_cache:
            # Execute and cache the result if not in cache
            result = func(*args, **kwargs)
            query_cache[query] = result
            return result
        else:
            # Return cached result if available
            return query_cache[query]
    return wrapper

def with_db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            # Pass the connection as the first argument if not already provided
            if 'conn' not in kwargs and not (len(args) > 0 and isinstance(args[0], sqlite3.Connection)):
                kwargs['conn'] = conn
            result = func(*args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")

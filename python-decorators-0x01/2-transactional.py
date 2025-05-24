import sqlite3
import functools

def with_db_connection(func):
    @functools.wraps(func)
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

def transactional(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        # Check if 'conn' is in kwargs or the first positional arg is a connection
        if 'conn' in kwargs:
            conn = kwargs['conn']
        elif len(args) > 0 and isinstance(args[0], sqlite3.Connection):
            conn = args[0]
        
        if not conn:
            raise ValueError("No database connection provided to the transactional decorator")
        
        try:
            result = func(*args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise e
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Update user's email with automatic transaction handling
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')

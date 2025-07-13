import time
import sqlite3 
import functools

#### decorator to handle caching

def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = args[1]
        if query in query_cache:
            return query_cache[query]
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

query_cache = {}

#### decorator to handle database connections
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        result = func(conn, *args, **kwargs)
        conn.close()
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
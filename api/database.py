import psycopg2
 
def connect_db():
    conn = psycopg2.connect(
        dbname='biblioteca',
        user='user',
        password='password',
        host='db',
        port='5432'
    )
    return conn

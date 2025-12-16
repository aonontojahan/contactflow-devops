import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="contactdb",
        user="postgres",
        password="aonontojahan",
        host="localhost",
        port="5432"
    )


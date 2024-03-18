import pg8000

DB_ENDPOINT = "localhost"
DB_USERNAME = "postgres"
DB_PASSWORD = "1234"
DB_DATABASE = "confa"

def connect_to_database():
    try:
        conn = pg8000.connect(
        host=DB_ENDPOINT,
        database=DB_DATABASE,
        user=DB_USERNAME,
        password=DB_PASSWORD)
        return conn
    except Exception as e:
        print(str(e))
        return None
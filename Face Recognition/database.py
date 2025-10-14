import psycopg2

def get_db_connection():
    return psycopg2.connect(
        dbname="FaceRecognition",
        user="postgres",
        password="123456",
        host="localhost",
        port="5432"
    )
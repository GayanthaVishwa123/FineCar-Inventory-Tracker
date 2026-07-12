import os

import psycopg2


def test_database_connection():
    # Pipline url connatct
    db_url = os.getenv("DATABASE_URL")
    try:
        conn = psycopg2.connect(db_url)
        print("Database connection successful!")
        conn.close()
    except Exception as e:
        print(f"Database connection failed: {e}")
        assert False, "Could not connect to database"

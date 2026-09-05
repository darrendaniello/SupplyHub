from sqlalchemy import text

from app.database import engine

def test_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))

        print("Database connected successfully!")
        print(result.scalar())

if __name__ == "__main__":
    test_connection()
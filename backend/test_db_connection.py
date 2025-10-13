import os
from sqlalchemy import create_engine, text

# Set your DATABASE_URL here for testing
DATABASE_URL = "postgresql://postgres:senhapostgree2@database.cz8oqcqu6dnv.us-east-2.rds.amazonaws.com:5432/database"

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Connection successful! Result:", result.fetchone())
except Exception as e:
    print("Connection failed:", str(e))
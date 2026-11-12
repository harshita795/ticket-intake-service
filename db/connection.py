import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

def check_db():
  with psycopg.connect(
    host="localhost",
    port=5432,
    dbname="postgres",
    user="postgres",
    password=os.getenv("POSTGRES_PASSWORD")
  ) as conn:
    with conn.cursor() as cur:
      cur.execute("SELECT 1;")
      return cur.fetchone()[0]
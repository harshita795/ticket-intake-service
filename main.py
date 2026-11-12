from fastapi import FastAPI
from db.connection import check_db

app = FastAPI()


@app.get("/health")
def health_check():
  db_result = check_db()
  return {"status":"ok", "db": db_result}

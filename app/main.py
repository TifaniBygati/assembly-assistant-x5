from fastapi import FastAPI
from app.local_base import data

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/clients")
def get_all_clients():
    return data
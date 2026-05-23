from fastapi import FastAPI,HTTPException
from app.local_base import data
from app.schemas import ClientCreate
from app.search_helpers import find_clients_by_address
from app.client_helpers import create_new_client

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/clients")
def get_all_clients():
    return data

@app.get("/clients/search")
def search_clients(street=None, house=None, apartment=None):
    result = find_clients_by_address(data ,street=street, house=house, apartment=apartment)
    if result == []:
        raise HTTPException(status_code=404,detail="User_not_found")
    return result
@app.post("/clients")
def create_client(client_data: ClientCreate):

    result = create_new_client(data,client_data)

    return result
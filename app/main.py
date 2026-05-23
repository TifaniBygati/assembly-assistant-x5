from fastapi import FastAPI,HTTPException
from app.local_base import data
from app.schemas import ClientCreate
from app.search_helpers import find_clients_by_address
from app.client_helpers import create_new_client,find_client_by_id

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

@app.get("/clients/{client_id}")
def get_client_by_id(
        client_id:int
):
    result = find_client_by_id(data,client_id)

    if result == None:
        raise HTTPException(status_code=404,detail="client_not_found")

    return result
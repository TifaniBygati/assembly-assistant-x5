from fastapi import FastAPI,HTTPException

from app.schemas import ClientCreate, ClientUpdate
from app.search_helpers import find_clients_by_address
from app.client_service import create_new_client,find_client_by_id,update_client,delete_client

from data.json_storage import load_data,save_data

data = load_data()
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
    save_data(data)
    return result

@app.get("/clients/{client_id}")
def get_client_by_id(
        client_id:int
):
    result = find_client_by_id(data,client_id)

    if result == None:
        raise HTTPException(status_code=404,detail="client_not_found")

    return result

@app.patch("/clients/{client_id}")
def update_client_by_id(
        client_id:int,
        new_client_data:ClientUpdate
):
    result = update_client(data, client_id,new_client_data)

    if result is None:
        raise HTTPException(status_code=404,detail="client_not_found")
    save_data(data)
    return result

@app.delete("/clients/{client_id}")
def delete_client_by_id(
        client_id:int
):
    result = delete_client(data,client_id)

    if result is None:
        raise HTTPException(status_code=404,detail="client_not_found")
    save_data(data)
    return result
from fastapi import APIRouter,HTTPException

from app.schemas import ClientCreate, ClientUpdate
from app.search_helpers import find_clients_by_address
from app.client_service import create_new_client,find_client_by_id,update_client,delete_client

from data.json_storage import load_data,save_data


router = APIRouter(prefix="/clients", tags=["clients"])

data = load_data()

@router.get("")
def get_all_clients():
    return data

@router.get("/search")
def search_clients(street=None, house=None, apartment=None):
    result = find_clients_by_address(data ,street=street, house=house, apartment=apartment)
    if result == []:
        raise HTTPException(status_code=404,detail="User_not_found")
    return result
@router.post("")
def create_client(client_data: ClientCreate):

    result = create_new_client(data,client_data)
    save_data(data)
    return result

@router.get("/{client_id}")
def get_client_by_id(
        client_id:int
):
    result = find_client_by_id(data,client_id)

    if result is None:
        raise HTTPException(status_code=404,detail="client_not_found")

    return result

@router.patch("/{client_id}")
def update_client_by_id(
        client_id:int,
        new_client_data:ClientUpdate
):
    result = update_client(data, client_id,new_client_data)

    if result is None:
        raise HTTPException(status_code=404,detail="client_not_found")
    save_data(data)
    return result

@router.delete("/{client_id}")
def delete_client_by_id(
        client_id:int
):
    result = delete_client(data,client_id)

    if result is None:
        raise HTTPException(status_code=404,detail="client_not_found")
    save_data(data)
    return result
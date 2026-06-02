from fastapi import APIRouter,HTTPException

from app.schemas import ClientCreate, ClientUpdate

from app.sqlite_service import (
    get_all_clients_from_db,
    get_client_by_id_from_db,
    patch_and_put_client_by_client_id_from_db,
    find_clients_by_address_from_db,
    create_new_client_from_db,
    delete_client_by_client_id_from_db
)

router = APIRouter(prefix="/clients", tags=["clients"])



@router.get("")
def get_all_clients():

    result = get_all_clients_from_db()

    return result

@router.get("/search")
def search_clients(street=None, house=None, apartment=None):
    result = find_clients_by_address_from_db(street=street, house=house, apartment=apartment)

    if result == []:
        raise HTTPException(status_code=404,detail="User_not_found")

    return result
@router.post("")
def create_client(client_data: ClientCreate):

    result = create_new_client_from_db(client_data)

    return result

@router.get("/{client_id}")
def get_client_by_id(
        client_id:int
):
    result = get_client_by_id_from_db(client_id)

    if result is None:
        raise HTTPException(status_code=404,detail="client_not_found")

    return result

@router.patch("/{client_id}")
def update_client_by_id(
        client_id: int,
        client_data: ClientUpdate
):
    update_data = client_data.model_dump(exclude_none=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="bad_request")

    result = patch_and_put_client_by_client_id_from_db(client_id, client_data)

    if result is None:
        raise HTTPException(status_code=404, detail="client_not_found")

    return result

@router.put("/{client_id}")
def update_client_full(
        client_data: ClientCreate,
        client_id:int
):
    result = patch_and_put_client_by_client_id_from_db(client_id, client_data)

    if result is None:
        raise HTTPException(status_code=400, detail="bad_request")

    return result


@router.delete("/{client_id}")
def delete_client_by_id(
        client_id:int
):
    result = delete_client_by_client_id_from_db(client_id)

    if not result:
        raise HTTPException(status_code=404,detail="client_not_found")

    return {'detail':"client_deleted"}
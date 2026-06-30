from fastapi import APIRouter,HTTPException

from app.schemas import (ClientCreate,
                         ClientAddressUpdatePATCH,
                         ClientUpdatePATCH,
                         ClientUpdatePUT,
                         AddressPut
                         )

from app.sqlite_service import (
    client_address_update,
    create_new_client_from_db,
    delete_client_from_db,
    client_update_from_db,
    client_put_db,
    address_put_db
)
from app.postgresql_service import (
    get_clients_from_postgres,
    get_client_by_id_from_postgre,
    search_clients_from_postgres,
    delete_client_from_postgres

)
router = APIRouter(prefix="/clients", tags=["clients"])



@router.get("")
def get_all_clients():

    result = get_clients_from_postgres()

    return result

@router.get("/search")
def search_clients(street=None, house=None, apartment=None):
    result = search_clients_from_postgres(street=street, house=house, apartment=apartment)

    if result is None:
        raise HTTPException(status_code=400, detail="no_input_params")

    if result == []:
        raise HTTPException(status_code=404,detail="client_not_found")

    return result
@router.post("")
def create_client(client_data: ClientCreate):

    result = create_new_client_from_db(client_data)

    return result

@router.get("/{client_id}")
def get_client_by_id(
        client_id:int
):
    result = get_client_by_id_from_postgre(client_id)

    if result == []:
        raise HTTPException(status_code=404,detail="client_not_found")

    return result

@router.patch("/addresses/{address_id}")
def update_address_by_id(
        address_id: int,
        client_data: ClientAddressUpdatePATCH
):
    update_data = client_data.model_dump(exclude_none=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="bad_request")

    result = client_address_update(address_id, client_data)

    if result is None:
        raise HTTPException(status_code=404, detail="address_not_found")

    return result

@router.patch("/{client_id}")
def update_client_by_id(client_id: int, client_data: ClientUpdatePATCH):

    update_data = client_data.model_dump(exclude_none=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="bad_request")

    result = client_update_from_db(client_id, client_data)

    if result is None:
        raise HTTPException(status_code=404, detail="client_not_found")

    return result


@router.put("/{client_id}")
def update_client(
        client_data: ClientUpdatePUT,
        client_id:int
):
    result = client_put_db(client_id, client_data)

    if result is None:
        raise HTTPException(status_code=404, detail="client_not_found")

    return result

@router.put("/addresses/{address_id}")
def update_address(
        address_data: AddressPut,
        address_id:int
):
    result = address_put_db(address_id, address_data)

    if result is None:
        raise HTTPException(status_code=404, detail="address_not_found")

    return result


@router.delete("/{client_id}")
def delete_client_by_id(
        client_id:int
):
    deleted_client_id  = delete_client_from_postgres(client_id)

    if deleted_client_id is None:
        raise HTTPException(status_code=404,detail="client_not_found")

    return {"deleted_client_id" : deleted_client_id}
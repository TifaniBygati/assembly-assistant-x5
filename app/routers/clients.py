from fastapi import APIRouter,HTTPException
from psycopg.errors import UniqueViolation

from app.response_helpers import group_clients_with_addresses

from app.schemas import (ClientCreate,
                         ClientAddressUpdatePATCH,
                         ClientUpdatePATCH,
                         ClientUpdatePUT,
                         AddressPut
                         )

from app.postgresql_service import (
    get_clients_from_postgres,
    get_client_by_id_from_postgre,
    search_clients_from_postgres,
    delete_client_from_postgres,
    create_client_from_postgres,
    client_update_patch_from_postgres,
    addresses_update_patch_from_postgres,
    client_update_put_from_postgres,
    addresses_update_put_from_postgres

)
router = APIRouter(prefix="/clients", tags=["clients"])



@router.get("")
def get_all_clients():

    rows = get_clients_from_postgres()

    group_result = group_clients_with_addresses(rows)

    return group_result

@router.get("/search")
def search_clients(street=None, house=None, apartment=None):

    rows = search_clients_from_postgres(street=street, house=house, apartment=apartment)

    if rows is None:
        raise HTTPException(status_code=400, detail="no_input_params")

    if rows == []:
        raise HTTPException(status_code=404,detail="client_not_found")

    group_result = group_clients_with_addresses(rows)

    return group_result
@router.post("", status_code=201)
def create_client(client_data: ClientCreate):

    rows = create_client_from_postgres(client_data)

    group_result = group_clients_with_addresses(rows)

    return group_result[0]

@router.get("/{client_id}")
def get_client_by_id(
        client_id:int
):
    rows = get_client_by_id_from_postgre(client_id)

    if rows == []:
        raise HTTPException(status_code=404,detail="client_not_found")

    group_result = group_clients_with_addresses(rows)

    return group_result[0]

@router.patch("/addresses/{address_id}")
def update_address_by_id(
        address_id: int,
        address_data: ClientAddressUpdatePATCH
):
    update_data = address_data.model_dump(exclude_none=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="no_update_fields")

    if update_data.get("street") == '':
        raise HTTPException(status_code=400, detail="invalid_street")

    if update_data.get("house") == '':
        raise HTTPException(status_code=400, detail="invalid_house")

    rows = addresses_update_patch_from_postgres(address_id, address_data)

    if rows is None:
        raise HTTPException(status_code=404, detail="address_not_found")

    group_result = group_clients_with_addresses(rows)

    return group_result[0]

@router.patch("/{client_id}")
def update_client_by_id(client_id: int, client_data: ClientUpdatePATCH):

    update_data = client_data.model_dump(exclude_none=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="no_update_fields")

    if update_data.get("phone") == '':
        raise HTTPException(status_code=400, detail="invalid_phone")

    try:
        rows = client_update_patch_from_postgres(client_id, client_data)
    except UniqueViolation:
        raise HTTPException(status_code=409, detail="phone_already_exists")

    if rows is None:
        raise HTTPException(status_code=404, detail="client_not_found")

    group_result = group_clients_with_addresses(rows)

    return group_result[0]


@router.put("/{client_id}")
def update_client(
        client_data: ClientUpdatePUT,
        client_id:int
):

    if client_data.name == '':
        raise HTTPException(status_code=400, detail="invalid_name")

    if client_data.phone == '':
        raise HTTPException(status_code=400, detail="invalid_phone")

    try:

        rows = client_update_put_from_postgres(client_id, client_data)

    except UniqueViolation:
        raise HTTPException(status_code=409, detail="phone_already_exists")

    if rows is None:
        raise HTTPException(status_code=404, detail="client_not_found")

    group_result = group_clients_with_addresses(rows)

    return group_result[0]

@router.put("/addresses/{address_id}")
def update_address(
        address_data: AddressPut,
        address_id:int
):

    if address_data.street == '':
        raise HTTPException(status_code=400, detail="invalid_street")

    if address_data.house == '':
        raise HTTPException(status_code=400, detail="invalid_house")

    rows = addresses_update_put_from_postgres(address_id, address_data)

    if rows is None:
        raise HTTPException(status_code=404, detail="address_not_found")

    group_result = group_clients_with_addresses(rows)

    return group_result[0]


@router.delete("/{client_id}")
def delete_client_by_id(
        client_id:int
):
    deleted_client_id  = delete_client_from_postgres(client_id)

    if deleted_client_id is None:
        raise HTTPException(status_code=404,detail="client_not_found")

    return {"deleted_client_id" : deleted_client_id}
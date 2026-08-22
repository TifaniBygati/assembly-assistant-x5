from fastapi import APIRouter,HTTPException

from psycopg.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from app.response_helpers import group_clients_with_addresses, group_clients_with_obj_orm, group_one_with_obj_orm

from app.schemas import (ClientCreate,
                         ClientAddressUpdatePATCH,
                         ClientUpdatePATCH,
                         ClientUpdatePUT,
                         AddressPut
                         )

from app.postgresql_service import (
    delete_client_from_postgres,
)

from app.sqlalchemy_service import (
    get_clients_from_orm,
    get_client_by_id_from_orm,
    search_clients_from_orm,
    create_client_from_orm,
    patch_client_from_orm,
    patch_address_from_orm,
    put_client_from_orm,
    put_address_from_orm

)

router = APIRouter(prefix="/clients", tags=["clients"])



@router.get("")
def get_all_clients():

    obj = get_clients_from_orm()

    if obj == []:
        raise HTTPException(status_code=404, detail="clients_not_found")

    result = group_clients_with_obj_orm(obj)

    return result

@router.get("/search")
def search_clients(street=None, house=None, apartment=None):

    obj = search_clients_from_orm(street=street, house=house, apartment=apartment)

    if obj is None:
        raise HTTPException(status_code=400, detail="no_input_params")

    result = group_clients_with_obj_orm(obj)
    if result == []:
        raise HTTPException(status_code=404, detail="no_clients_found")

    return result
@router.post("", status_code=201)
def create_client(client_data: ClientCreate):
    obj = create_client_from_orm(client_data)

    result = group_one_with_obj_orm(obj)

    return result

@router.get("/{client_id}")
def get_client_by_id(
        client_id:int
):
    obj = get_client_by_id_from_orm(client_id)

    if obj is None:
        raise HTTPException(status_code=404, detail="client_not_found")

    result = group_one_with_obj_orm(obj)

    return result


@router.patch("/addresses/{address_id}")
def update_address_by_id(
        address_id: int,
        address_data: ClientAddressUpdatePATCH
):

    new_address_data = address_data.model_dump(exclude_none=True)

    if not new_address_data:
        raise HTTPException(status_code=400, detail="no_update_fields")

    for item, value in new_address_data.items():
        if value == '':
            raise HTTPException(status_code=400, detail=f"invalid_{item}")

    obj = patch_address_from_orm(address_id, new_address_data)

    if obj is None:
        raise HTTPException(status_code=404, detail="address_not_found")

    result = group_one_with_obj_orm(obj)

    return result


@router.patch("/{client_id}")
def update_client_by_id(client_id: int, client_data: ClientUpdatePATCH):

    new_client_data = client_data.model_dump(exclude_none=True)

    if not new_client_data:
        raise HTTPException(status_code=400, detail="no_update_fields")

    for item, value in new_client_data.items():
        if value == '':
            raise HTTPException(status_code=400, detail=f"invalid_{item}")
    try:

        obj = patch_client_from_orm(client_id, new_client_data)

    except IntegrityError as exc:
        if isinstance(exc.orig, UniqueViolation):
            raise HTTPException(status_code=409, detail="phone_already_exists")

        raise

    if obj is None:
        raise HTTPException(status_code=404, detail="client_not_found")

    result = group_one_with_obj_orm(obj)

    return result



@router.put("/{client_id}")
def update_client(
        client_id: int,
        client_data: ClientUpdatePUT
):

    for item, value in client_data.model_dump().items():
        if value == '':
            raise HTTPException(status_code=400, detail=f"invalid_{item}")

    try:

        obj = put_client_from_orm(client_id, client_data)

    except IntegrityError as exc:
        if isinstance(exc.orig, UniqueViolation):
            raise HTTPException(status_code=409, detail="phone_already_exists")
        raise

    if obj is None:
        raise HTTPException(status_code=404, detail="client_not_found")

    result = group_one_with_obj_orm(obj)

    return result


@router.put("/addresses/{address_id}")
def update_address(
        address_id:int,
        address_data: AddressPut
):

    new_address_data = address_data.model_dump()

    for item, value in new_address_data.items():
        if value == '':
            raise HTTPException(status_code=400, detail=f"invalid_{item}")

    obj = put_address_from_orm(address_id, new_address_data)

    if obj is None:
        raise HTTPException(status_code=404, detail="address_not_found")

    result = group_one_with_obj_orm(obj)

    return result

@router.delete("/{client_id}")
def delete_client_by_id(
        client_id:int
):
    deleted_client_id  = delete_client_from_postgres(client_id)

    if deleted_client_id is None:
        raise HTTPException(status_code=404,detail="client_not_found")

    return {"deleted_client_id" : deleted_client_id}
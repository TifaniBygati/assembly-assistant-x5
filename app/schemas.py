from pydantic import BaseModel

class ClientCreate(BaseModel):
    name: str | None = None
    phone: str
    street: str
    house: str
    floor: str | None = None
    entrance: str | None = None
    apartment: str | None = None
    comment: str | None = None

class ClientAddressUpdatePATCH(BaseModel):
    street: str | None = None
    house: str | None = None
    floor: str | None = None
    entrance: str | None = None
    apartment: str | None = None
    comment: str | None = None

class ClientUpdatePATCH(BaseModel):
    name: str | None = None
    phone: str | None = None

class ClientUpdatePUT(BaseModel):
    name: str
    phone: str

class AddressPut(BaseModel):
    street: str
    house: str
    floor: str | None = None
    entrance: str | None = None
    apartment: str | None = None
    comment: str | None = None
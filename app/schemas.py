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





class ClientUpdate(BaseModel):
    order_id: str | None = None
    street: str | None = None
    house: str | None = None
    apartment: str | None = None
    phone: str | None = None
    comment: str | None = None
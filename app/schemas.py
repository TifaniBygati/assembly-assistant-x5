from pydantic import BaseModel

class ClientCreate(BaseModel):
    order_id: str
    street: str
    house: str
    apartment: str
    phone: str
    comment: str | None = None

class ClientUpdate(BaseModel):
    order_id: str | None = None
    street: str | None = None
    house: str | None = None
    apartment: str | None = None
    phone: str | None = None
    comment: str | None = None
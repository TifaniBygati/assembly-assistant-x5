from pydantic import BaseModel

class ClientCreate(BaseModel):
    order_id: str
    street: str
    house: str
    apartment: str
    phone: str
    comment: str | None = None
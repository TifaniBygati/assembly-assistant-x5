from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session,
    joinedload,
    contains_eager

)

from sqlalchemy import (
    Text,
    CheckConstraint,
    ForeignKey,
    create_engine,
    select
)

import os

class Base(DeclarativeBase):
    pass

class Client(Base):
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str | None] = mapped_column(
        Text,
        CheckConstraint(
            "name <> ''",
            name="clients_name_not_empty"
        ),

    )

    phone: Mapped[str] = mapped_column(
        Text,
        CheckConstraint(
            "phone <> ''",
            name="clients_phone_not_empty"
        ),
        unique=True
    )

    addresses: Mapped[list['Address']] = relationship(
        back_populates='client'
    )

class Address(Base):
    __tablename__ = 'addresses'

    id: Mapped[int] = mapped_column(primary_key=True)

    client_id: Mapped[int] = mapped_column(
        ForeignKey(
'clients.id',
        ondelete='CASCADE')
    )

    street: Mapped[str] = mapped_column(
        Text,
        CheckConstraint(
            "street <> ''",
            name="addresses_street_not_empty"
        )
    )

    house: Mapped[str] = mapped_column(
        Text,
        CheckConstraint(
            "house <> ''",
            name="addresses_house_not_empty"
        )
    )

    floor: Mapped[str | None] = mapped_column(
        Text,
        CheckConstraint(
            "floor <> ''",
            name="addresses_floor_not_empty"
        )
    )

    entrance: Mapped[str | None] = mapped_column(
        Text,
        CheckConstraint(
            "entrance <> ''",
            name="addresses_entrance_not_empty"
        )
    )

    apartment: Mapped[str | None] = mapped_column(
        Text,
        CheckConstraint(
            "apartment <> ''",
            name="addresses_apartment_not_empty"
        )
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        CheckConstraint(
            "comment <> ''",
            name="addresses_comment_not_empty"
        )
    )

    client: Mapped['Client'] = relationship(
        back_populates='addresses'
    )

def get_engine():
    DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
    DB_PORT = int(os.getenv('DB_PORT', '5433'))
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'localbase')
    DB_NAME = os.getenv('DB_NAME', 'assembly_assistant_x5_dev')

    return create_engine(f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

def get_client_by_id_from_orm(client_id):

    engine = get_engine()

    with Session(engine) as session:
        client = (
            session.execute(
                select(Client)
                .where(Client.id == client_id)
                .options(
                    joinedload(Client.addresses))
            )
            .unique()
            .scalars()
            .first()
        )

        return client

def get_clients_from_orm():

    engine = get_engine()

    with Session(engine) as session:
        clients = (
            session.execute(
                select(Client)
                .options(
                    joinedload(Client.addresses)
                )
            )
            .unique()
            .scalars()
            .all()
        )
        return clients

def search_clients_from_orm(street=None, house=None, apartment=None):

    if street is None and house is None and apartment is None:
        return None

    conditions = []

    if street is not None:
        conditions.append(Address.street == street)

    if house is not None:
        conditions.append(Address.house == house)

    if apartment is not None:
        conditions.append(Address.apartment == apartment)

    engine = get_engine()

    with Session(engine) as session:
        clients = (
            session.execute(
                select(Client)
                .join(Address)
                .where(*conditions)
                .options(
                    contains_eager(Client.addresses)
                )
            )
            .unique()
            .scalars()
            .all()
        )

    return clients

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
        back_populates='client',
        passive_deletes=True
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

def build_address(client_data, client):

    new_address_data = Address(
        street=client_data.street,
        house=client_data.house,
        floor=client_data.floor,
        entrance=client_data.entrance,
        apartment=client_data.apartment,
        comment=client_data.comment,
        client=client,
    )

    return new_address_data

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

def create_client_from_orm(client_data):

    engine = get_engine()

    with Session(engine) as session:

        client = (
            session.execute(
                select(Client)
                .where(Client.phone == client_data.phone)
            )
            .scalars()
            .first()
        )
        if client is None:

            client = Client(
                name=client_data.name,
                phone=client_data.phone,
            )
            session.add(client)

        new_address_data = build_address(client_data, client)
        session.add(new_address_data)

        session.flush()

        client_id = client.id

        session.commit()

        return get_client_by_id_from_orm(client_id)

def patch_client_from_orm(client_id, new_client_data):

    engine = get_engine()

    with Session(engine) as session:
        client = (
            session.execute(
                select(Client)
                .where(Client.id == client_id)
            )
            .scalars()
            .first()
        )

        if client is None:
            return None

        for name, value in new_client_data.items():
            setattr(client, name, value)

        session.commit()

        return get_client_by_id_from_orm(client_id)

def patch_address_from_orm(address_id, new_address_data):

    engine = get_engine()

    with Session(engine) as session:
        address = (
            session.execute(
                select(Address)
                .where(Address.id == address_id)
            )
            .scalars()
            .first()
        )
        if address is None:
            return None

        for name, value in new_address_data.items():
            setattr(address, name, value)

        client_id = address.client_id

        session.commit()

        return get_client_by_id_from_orm(client_id)

def put_client_from_orm(client_id, new_client_data):

    engine = get_engine()

    with Session(engine) as session:
        client = (
            session.execute(
                select(Client)
                .where(Client.id == client_id)
            )
            .scalars()
            .first()
        )

        if client is None:
            return None

        client.name = new_client_data.name
        client.phone = new_client_data.phone

        session.commit()

    return get_client_by_id_from_orm(client_id)

def put_address_from_orm(address_id, new_address_data):

    engine = get_engine()
    with Session(engine) as session:
        address = (
            session.execute(
                select(Address)
                .where(Address.id == address_id)
            )
            .scalars()
            .first()
        )

        if address is None:
            return None

        for name, value in new_address_data.items():
            setattr(address, name, value)

        client_id = address.client_id

        session.commit()

    return get_client_by_id_from_orm(client_id)

def delete_client_from_orm(client_id):

    engine = get_engine()

    with Session(engine) as session:
        client = (
            session.execute(
                select(Client)
                .where(Client.id == client_id)
            )
            .scalars()
            .first()
        )
        if client is None:
            return None

        session.delete(client)

        client_id = client.id

        session.commit()

        return client_id
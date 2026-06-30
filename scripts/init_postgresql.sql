CREATE TABLE IF NOT EXISTS clients (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    name TEXT
        CONSTRAINT clients_name_not_empty CHECK (name <> ''),

    phone TEXT
        CONSTRAINT clients_phone_not_null NOT NULL
        CONSTRAINT clients_phone_unique UNIQUE
        CONSTRAINT clients_phone_not_empty CHECK (phone <> '')
);

CREATE TABLE IF NOT EXISTS addresses (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    client_id INTEGER
        CONSTRAINT addresses_client_id_not_null NOT NULL,

    street TEXT
        CONSTRAINT addresses_street_not_null NOT NULL
        CONSTRAINT addresses_street_not_empty CHECK (street <> ''),

    house TEXT
        CONSTRAINT addresses_house_not_null NOT NULL
        CONSTRAINT addresses_house_not_empty CHECK (house <> ''),

    floor TEXT
        CONSTRAINT addresses_floor_not_empty CHECK (floor <> ''),

    entrance TEXT
        CONSTRAINT addresses_entrance_not_empty CHECK (entrance <> ''),

    apartment TEXT
        CONSTRAINT addresses_apartment_not_empty CHECK (apartment <> ''),

    comment TEXT
        CONSTRAINT addresses_comment_not_empty CHECK (comment <> ''),

    CONSTRAINT addresses_client_id_fk
        FOREIGN KEY (client_id)
        REFERENCES clients(id)
        ON DELETE CASCADE
);


CREATE INDEX IF NOT EXISTS addresses_client_id_idx
ON addresses(client_id);
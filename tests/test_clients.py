from fastapi.testclient import TestClient
from app.main import app
from tests.helpers.helpers import setup_test_database

client = TestClient(app)

def get_clients_body():
    response = client.get("/clients")
    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert body != []

    return body

def get_first_client():
    clients = get_clients_body()
    return clients[0]

def get_first_client_id():
    clients = get_first_client()
    return clients['client_id']

def get_first_address():
    first_client = get_first_client()

    assert 'addresses' in first_client
    assert isinstance(first_client['addresses'], list)
    assert first_client['addresses'] != []

    return first_client['addresses'][0]

def get_first_address_id():
    first_client = get_first_address()
    return first_client['address_id']


def test_get_clients(monkeypatch):

    setup_test_database(monkeypatch)

    response = client.get("/clients")

    assert response.status_code == 200
    body = response.json()

    assert isinstance(body, list)
    assert body != []

def test_get_client_by_id(monkeypatch):

    setup_test_database(monkeypatch)

    client_id = get_first_client_id()

    response = client.get(f'/clients/{client_id}')

    body = response.json()

    assert response.status_code == 200
    assert isinstance(body, dict)
    assert body['client_id'] == client_id
    assert 'name' in body
    assert 'phone' in body
    assert 'addresses' in body
    assert isinstance(body['addresses'], list)

def test_get_client_by_address(monkeypatch):

    setup_test_database(monkeypatch)

    first_address = get_first_address()

    street = first_address['street']
    house = first_address['house']

    response = client.get('/clients/search', params={'street': street, 'house': house})

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert body != []

    found_addresses_count = 0

    for client_item in body:
        assert 'addresses' in client_item
        assert isinstance(client_item['addresses'], list)

        for address in client_item['addresses']:
            found_addresses_count += 1

            assert 'street' in address
            assert 'house' in address

            assert address['street'] == street
            assert address['house'] == house

    assert found_addresses_count > 0

def test_clients_from_test_database(monkeypatch):

    setup_test_database(monkeypatch)

    body = get_clients_body()

    assert len(body) == 2

    phones = {client['phone'] for client in body}

    assert phones == {'+79990000001', '+79990000002'}

def test_create_client_in_test_database(monkeypatch):

    setup_test_database(monkeypatch)

    payload = {
        'name': 'Петя',
        'phone': '+79990000003',
        'street': 'Ленина',
        'house': '5',
        'floor': '2',
        'entrance': '1',
        'apartment': '10',
        'comment': 'тестовый клиент'
    }

    response = client.post('/clients', json=payload)

    assert response.status_code == 201

    body = response.json()

    assert isinstance(body, dict)

    assert body['name'] == payload['name']
    assert body['phone'] == payload['phone']
    assert body['addresses'] != []

    client_id = body['client_id']

    response = client.get(f'/clients/{client_id}')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)
    assert body['phone'] == payload['phone']
    assert body['name'] == payload['name']
    assert body['addresses'] != []

    body = get_clients_body()

    assert len(body) >= 3

    phones = {client_data['phone'] for client_data in body}

    assert payload['phone'] in phones

def test_patch_client_in_test_database(monkeypatch):

    payload = {
        'name': 'test_patch_name',
        'phone': 'test_patch_phone',
    }

    setup_test_database(monkeypatch)

    first_client_id = get_first_client_id()

    response = client.get(f'/clients/{first_client_id}')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)

    assert 'name' in body
    assert 'phone' in body
    assert body['addresses'] != []

    old_name = body['name']
    old_phone = body['phone']

    response = client.patch(f'/clients/{first_client_id}', json=payload)

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)


    assert body['client_id'] == first_client_id

    assert body['name'] != old_name
    assert body['phone'] != old_phone

    assert body['name'] == payload['name']
    assert body['phone'] == payload['phone']

    response = client.get(f'/clients/{first_client_id}')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)

    assert body['name'] == payload['name']
    assert body['phone'] == payload['phone']

def test_patch_address_in_test_database(monkeypatch):

    payload = {
        'street':'Мира',
        'house':'5',
        'floor':'2',
        'entrance':'1',
        'apartment':'10'
    }

    setup_test_database(monkeypatch)

    address_id = get_first_address_id()

    response = client.patch(f'/clients/addresses/{address_id}', json=payload)

    assert response.status_code == 200

    body = response.json()



    assert isinstance(body, dict)

    assert 'client_id' in body
    client_id = body['client_id']

    assert body['addresses'][0]['address_id'] == address_id

    assert body['addresses'][0]['street'] == payload['street']
    assert body['addresses'][0]['house'] == payload['house']
    assert body['addresses'][0]['floor'] == payload['floor']
    assert body['addresses'][0]['entrance'] == payload['entrance']
    assert body['addresses'][0]['apartment'] == payload['apartment']

    response = client.get(f'/clients/{client_id}')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)

    assert body['addresses'][0]['address_id'] == address_id

    assert body['addresses'][0]['street'] == payload['street']
    assert body['addresses'][0]['house'] == payload['house']
    assert body['addresses'][0]['floor'] == payload['floor']
    assert body['addresses'][0]['entrance'] == payload['entrance']
    assert body['addresses'][0]['apartment'] == payload['apartment']

def test_put_client_in_test_database(monkeypatch):

    payload = {
        'name': 'test_put_name',
        'phone': 'test_put_phone'
    }

    setup_test_database(monkeypatch)

    client_id = get_first_client_id()

    response = client.put(f'/clients/{client_id}', json=payload)

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)
    assert 'client_id' in body
    assert 'name' in body
    assert 'phone' in body

    assert body['client_id'] == client_id
    assert body['name'] == payload['name']
    assert body['phone'] == payload['phone']

    response = client.get(f'/clients/{client_id}')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)

    assert 'client_id' in body
    assert 'name' in body
    assert 'phone' in body


    assert body['name'] == payload['name']
    assert body['phone'] == payload['phone']

def test_put_address_in_test_database(monkeypatch):

    payload = {
        'street': 'Мира',
        'house': '77',
        'floor': None,
        'entrance': None,
        'apartment': None,
        'comment': 'частный дом'
    }

    setup_test_database(monkeypatch)

    client_id = get_first_client_id()

    response = client.get(f'/clients/{client_id}')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)

    assert 'client_id' in body
    assert 'name' in body
    assert 'phone' in body


    address_id = body['addresses'][0]['address_id']

    response = client.put(f'/clients/addresses/{address_id}', json=payload)

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)
    address = body['addresses'][0]

    assert address['street'] == payload['street']
    assert address['house'] == payload['house']
    assert address['comment'] == payload['comment']
    assert address['floor'] == payload['floor']
    assert address['entrance'] == payload['entrance']
    assert address['apartment'] == payload['apartment']

    response = client.get(f'/clients/{client_id}')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)

    address = body['addresses'][0]

    assert address['street'] == payload['street']
    assert address['house'] == payload['house']
    assert address['floor'] == payload['floor']
    assert address['entrance'] == payload['entrance']
    assert address['apartment'] == payload['apartment']
    assert address['comment'] == payload['comment']

def test_delete_client_in_test_database(monkeypatch):

    setup_test_database(monkeypatch)

    client_id = get_first_client_id()

    response = client.get(f'/clients/{client_id}')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)

    assert 'client_id' in body
    assert 'name' in body
    assert 'phone' in body
    assert body['addresses'] != []


    response = client.delete(f'/clients/{client_id}')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)
    assert body == {'deleted_client_id': client_id}

    response = client.get(f'/clients/{client_id}')

    assert response.status_code == 404

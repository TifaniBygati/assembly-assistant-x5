from fastapi.testclient import TestClient
from tests.helpers.helpers import setup_test_database
from app.main import app

client = TestClient(app)


def test_get_unknown_client_returns_404(monkeypatch):

    setup_test_database(monkeypatch)

    response = client.get("/clients")

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert body != []

    max_client_id = max(client_data["client_id"] for client_data in body)
    unknown_client_id = max_client_id + 1

    response = client.get(f"/clients/{unknown_client_id}")

    assert response.status_code == 404

def test_delete_unknown_client_returns_404(monkeypatch):

    setup_test_database(monkeypatch)

    response = client.get('/clients')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert body != []

    initial_clients_count = len(body)

    max_client_id = max(client_data["client_id"] for client_data in body)
    unknown_client_id = max_client_id + 1

    response = client.delete(f"/clients/{unknown_client_id}")

    assert response.status_code == 404

    body = response.json()

    assert body == {'detail': 'client_not_found'}

    response = client.get("/clients")

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert initial_clients_count == len(body)

def test_patch_unknown_client_returns_404(monkeypatch):

    payload = {
        'name': 'unknown_name',
        'phone': '+79990009999'
    }

    setup_test_database(monkeypatch)

    response = client.get('/clients')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert body != []

    max_client_id = max(client_data["client_id"] for client_data in body)
    unknown_client_id = max_client_id + 1

    response = client.patch(f"/clients/{unknown_client_id}", json=payload)

    assert response.status_code == 404

    body = response.json()

    assert body == {'detail': 'client_not_found'}

def test_patch_unknown_address_returns_404(monkeypatch):
    payload = {
        'street': 'test_street',
        'house': 'test_house'
    }

    setup_test_database(monkeypatch)

    response = client.get('/clients')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert body != []

    addresses_id = []

    for client_data in body:
        assert 'addresses' in client_data
        assert isinstance(client_data['addresses'], list)

        for address in client_data["addresses"]:
            assert 'address_id' in address
            addresses_id.append(address["address_id"])

    assert addresses_id != []

    max_address_id = max(addresses_id)
    unknown_address_id = max_address_id + 1

    response = client.patch(f"/clients/addresses/{unknown_address_id}", json=payload)

    assert response.status_code == 404

    body = response.json()

    assert body == {'detail': 'address_not_found'}

def test_patch_address_no_update_fields_returns_400(monkeypatch):

    payload = {
        'bad_street': '345456',
        'bad_house': '+79990009999'
    }

    setup_test_database(monkeypatch)

    response = client.get('/clients')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert body != []

    client_id = body[0]['client_id']

    response = client.get(f"/clients/{client_id}")

    body = response.json()

    assert response.status_code == 200
    assert isinstance(body, dict)

    assert 'client_id' in body
    assert 'name' in body
    assert 'phone' in body
    assert 'addresses' in body
    assert body['addresses'] != []


    address_id = body['addresses'][0]['address_id']

    response = client.patch(f"/clients/addresses/{address_id}", json=payload)

    assert response.status_code == 400

    body = response.json()

    assert body == {'detail': 'no_update_fields'}

def test_patch_address_invalid_street_returns_400(monkeypatch):

    setup_test_database(monkeypatch)

    response = client.get('/clients')

    assert response.status_code == 200
    body = response.json()

    assert isinstance(body, list)
    assert body != []

    client_id = body[0]['client_id']

    response = client.get(f"/clients/{client_id}")

    body = response.json()

    assert response.status_code == 200
    assert isinstance(body, dict)

    assert 'client_id' in body
    assert 'name' in body
    assert 'phone' in body
    assert 'addresses' in body
    assert body['addresses'] != []

    address = body['addresses'][0]

    address_id = address['address_id']

    response = client.patch(f"/clients/addresses/{address_id}", json={'street': ''})

    assert response.status_code == 400
    assert response.json() == {'detail': 'invalid_street'}

def test_patch_address_invalid_house_returns_400(monkeypatch):

    setup_test_database(monkeypatch)

    response = client.get('/clients')

    assert response.status_code == 200
    body = response.json()

    assert isinstance(body, list)
    assert body != []

    client_id = body[0]['client_id']

    response = client.get(f"/clients/{client_id}")

    body = response.json()

    assert response.status_code == 200
    assert isinstance(body, dict)

    assert 'client_id' in body
    assert 'name' in body
    assert 'phone' in body
    assert 'addresses' in body
    assert body['addresses'] != []

    address = body['addresses'][0]


    address_id = address['address_id']

    response = client.patch(f"/clients/addresses/{address_id}", json={'house': ''})

    assert response.status_code == 400
    assert response.json() == {'detail': 'invalid_house'}

def test_patch_client_no_update_fields_returns_400(monkeypatch):

    payload = {
        'bad_name': '345456',
        'bad_phone': '+79990009999'
    }

    setup_test_database(monkeypatch)

    response = client.get('/clients')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert body != []

    client_id = body[0]['client_id']

    response = client.patch(f"/clients/{client_id}", json=payload)

    assert response.status_code == 400

    body = response.json()

    assert body == {'detail': 'no_update_fields'}

def test_patch_client_invalid_phone_returns_400(monkeypatch):

    setup_test_database(monkeypatch)

    response = client.get('/clients')

    assert response.status_code == 200
    body = response.json()

    assert isinstance(body, list)
    assert body != []

    client_id = body[0]['client_id']

    response = client.get(f"/clients/{client_id}")

    body = response.json()

    assert response.status_code == 200
    assert isinstance(body, dict)

    assert 'client_id' in body
    assert 'name' in body
    assert 'phone' in body
    assert 'addresses' in body
    assert body['addresses'] != []


    response = client.patch(f"/clients/{client_id}", json={'phone': ''})

    assert response.status_code == 400
    assert response.json() == {'detail': 'invalid_phone'}

def test_patch_client_phone_already_exists_returns_409(monkeypatch):
    setup_test_database(monkeypatch)

    response = client.get('/clients')

    assert response.status_code == 200

    body = response.json()
    assert isinstance(body, list)
    assert body != []
    assert len(body) >= 2

    phone = body[0]['phone']
    client_id = body[1]['client_id']

    response = client.patch(f"/clients/{client_id}", json={'phone': phone})

    assert response.status_code == 409
    body = response.json()
    assert isinstance(body, dict)
    assert body == {'detail' : 'phone_already_exists'}

def test_put_client_unknown_id_returns_404(monkeypatch):
    payload = {
        'name': 'put_unknown_name',
        'phone': '+79990008888'
    }

    setup_test_database(monkeypatch)

    response = client.get('/clients')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert body != []

    max_client_id = max([client_data["client_id"] for client_data in body])
    unknown_client_id = max_client_id + 1

    response = client.put(f"/clients/{unknown_client_id}", json=payload)

    assert response.status_code == 404

    body = response.json()

    assert body == {'detail': 'client_not_found'}

def test_put_address_unknown_id_returns_404(monkeypatch):
    payload = {
        'street': 'put_unknown_street',
        'house': 'put_unknown_house'
    }

    setup_test_database(monkeypatch)

    response = client.get('/clients')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert body != []

    address_id = []

    for client_data in body:
        assert 'addresses' in client_data
        assert isinstance(client_data['addresses'], list)

        for address_data in client_data['addresses']:
            assert 'address_id' in address_data
            address_id.append(address_data['address_id'])

    max_address_id = max(address_id)

    unknown_address_id = max_address_id + 1

    response = client.put(f"/clients/addresses/{unknown_address_id}", json=payload)

    assert response.status_code == 404

    body = response.json()

    assert body == {'detail': 'address_not_found'}

def test_put_client_invalid_payload_returns_422(monkeypatch):
    payload = {
        '423feds': 'wef2ww3edwsca',
        'f4r3e4e': '+ewsdf32'
    }

    setup_test_database(monkeypatch)

    response = client.get('/clients')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert body != []

    client_id = body[0]['client_id']

    response = client.put(f"/clients/{client_id}", json=payload)

    assert response.status_code == 422

    body = response.json()

    assert 'detail' in body

def test_put_address_invalid_payload_returns_422(monkeypatch):
    payload = {
        '423feds': 'wef2ww3edwsca',
        'f4r3e4e': '+ewsdf32'
    }

    setup_test_database(monkeypatch)

    response = client.get('/clients')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert body != []

    address_id = body[0]['addresses'][0]['address_id']

    response = client.put(f"/clients/addresses/{address_id}", json=payload)

    assert response.status_code == 422

    body = response.json()

    assert 'detail' in body

def test_put_client_invalid_name_returns_400(monkeypatch):
    setup_test_database(monkeypatch)

    response = client.get('/clients')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert body != []
    assert len(body) == 2

    client_id = body[0]['client_id']

    response = client.put(f"/clients/{client_id}", json={'name': '', 'phone': '+79005001020'})

    assert response.status_code == 400
    assert response.json() == {'detail': 'invalid_name'}

def test_put_client_invalid_phone_returns_400(monkeypatch):
    setup_test_database(monkeypatch)

    response = client.get('/clients')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert body != []
    assert len(body) == 2

    client_id = body[0]['client_id']

    response = client.put(f"/clients/{client_id}", json={'name': 'Иван', 'phone': ''})

    assert response.status_code == 400
    assert response.json() == {'detail': 'invalid_phone'}

def test_put_address_invalid_street_returns_400(monkeypatch):

    setup_test_database(monkeypatch)

    response = client.get('/clients')

    assert response.status_code == 200

    body = response.json()
    assert isinstance(body, list)
    assert body != []

    address_id = body[0]['addresses'][0]['address_id']

    response = client.put(f"/clients/addresses/{address_id}", json={'street': '', 'house': '7'})

    assert response.status_code == 400
    assert response.json() == {'detail': 'invalid_street'}

def test_put_address_invalid_house_returns_400(monkeypatch):

    setup_test_database(monkeypatch)

    response = client.get('/clients')

    assert response.status_code == 200

    body = response.json()
    assert isinstance(body, list)
    assert body != []

    address_id = body[0]['addresses'][0]['address_id']

    response = client.put(f"/clients/addresses/{address_id}", json={'street': 'Мира', 'house': ''})

    assert response.status_code == 400
    assert response.json() == {'detail': 'invalid_house'}

def test_put_client_phone_already_exists_returns_409(monkeypatch):

    setup_test_database(monkeypatch)

    response = client.get('/clients')

    assert response.status_code == 200

    body = response.json()
    assert isinstance(body, list)
    assert body != []
    assert len(body) >= 2

    client_id = body[0]['client_id']
    phone = body[1]['phone']

    response = client.put(f"/clients/{client_id}", json={'name': 'string', 'phone': phone})

    assert response.status_code == 409
    body = response.json()
    assert isinstance(body, dict)
    assert body == {'detail': 'phone_already_exists'}

def test_post_client_missing_phone_returns_422(monkeypatch):

    payload = {
      "name": "good",
      "street": "good",
      "house": "good",
      "floor": "good",
      "entrance": "good",
      "apartment": "good",
      "comment": "good"
    }

    setup_test_database(monkeypatch)

    response = client.post("/clients", json=payload)

    assert response.status_code == 422

    body = response.json()

    assert isinstance(body, dict)

    assert 'detail' in body









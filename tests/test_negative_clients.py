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

    max_address_id = max([client_data["address_id"] for client_data in body])
    unknown_address_id = max_address_id + 1

    response = client.patch(f"/clients/addresses/{unknown_address_id}", json=payload)

    assert response.status_code == 404

    body = response.json()

    assert body == {'detail': 'address_not_found'}

def test_patch_bad_request_client_returns_400(monkeypatch):

    payload = {
        'bad_name': 345456,
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

    assert body == {'detail': 'bad_request'}

def test_patch_bad_request_address_returns_400(monkeypatch):

    payload = {
        'bad_street': 41,
        'bad_house': 'test_house'
    }

    setup_test_database(monkeypatch)

    response = client.get('/clients')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert body != []

    client_id = body[0]['client_id']

    response = client.patch(f"/clients/addresses/{client_id}", json=payload)

    assert response.status_code == 400

    body = response.json()

    assert body == {'detail': 'bad_request'}

def test_put_unknown_client_returns_404(monkeypatch):
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

def test_put_unknown_address_returns_404(monkeypatch):
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

    max_address_id = max([client_data["address_id"] for client_data in body])
    unknown_address_id = max_address_id + 1

    response = client.put(f"/clients/addresses/{unknown_address_id}", json=payload)

    assert response.status_code == 404

    body = response.json()

    assert body == {'detail': 'address_not_found'}

def test_put_client_with_invalid_payload_returns_422(monkeypatch):
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

    max_client_id = max([client_data["client_id"] for client_data in body])
    unknown_client_id = max_client_id + 1

    response = client.put(f"/clients/{unknown_client_id}", json=payload)

    assert response.status_code == 422

    body = response.json()

    assert 'detail' in body

def test_put_address_with_invalid_payload_returns_422(monkeypatch):
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

    max_address_id = max([client_data["address_id"] for client_data in body])
    unknown_address_id = max_address_id + 1

    response = client.put(f"/clients/addresses/{unknown_address_id}", json=payload)

    assert response.status_code == 422

    body = response.json()

    assert 'detail' in body

def test_create_client_without_phone_returns_422(monkeypatch):

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

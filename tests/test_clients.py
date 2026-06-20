from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_clients():
    response = client.get('/clients')

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_client_by_id():
    response = client.get('/clients')

    assert response.status_code == 200

    clients = response.json()

    assert clients != []

    client_id = clients[0]['client_id']

    response = client.get(f'/clients/{client_id}')

    body = response.json()

    assert response.status_code == 200
    assert isinstance(body, list)
    assert body[0]['client_id'] == client_id

def test_get_client_by_address():

    response = client.get('/clients')

    assert response.status_code == 200

    clients = response.json()

    assert clients != []

    client_id = clients[0]['client_id']

    response = client.get(f'/clients/{client_id}')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert body != []
    assert body[0]['client_id'] == client_id

    street = body[0]['street']
    house = body[0]['house']

    response = client.get('/clients/search', params={'street': street, 'house': house})

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert body != []
    assert body[0]['street'] == street
    assert body[0]['house'] == house

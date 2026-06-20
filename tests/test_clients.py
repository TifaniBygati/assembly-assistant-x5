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
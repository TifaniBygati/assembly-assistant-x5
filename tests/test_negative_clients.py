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

    max_client_id  = max(client_data["client_id"] for client_data in body)
    unknown_client_id  = max_client_id  + 1

    response = client.get(f"/clients/{unknown_client_id }")

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
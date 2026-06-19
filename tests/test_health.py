from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}

def test_unknown_get():
    response = client.get("/unknown")

    assert response.status_code == 404

test_health()
test_unknown_get()

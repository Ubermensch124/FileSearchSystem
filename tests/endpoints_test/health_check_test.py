from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    response = client.get("http://localhost/api/ping")

    assert response.status_code == 200
    assert response.json()['Result'] == "pong"

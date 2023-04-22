import time
from datetime import timedelta, datetime

from fastapi.testclient import TestClient


def test_post(client: TestClient):
    data = {
        "text": "abra",
        "file_mask": "*.*",
        "size": {
            "value": 42000000,
            "operator": "le"
        },
        "creation_time": {
            "value": str(datetime.now()+timedelta(days=1)),
            "operator": "le"
        }
    }
    response = client.post("http://localhost/search", json=data)

    assert response.status_code == 200
    assert ("search_id" in response.json()) == True


def test_get(client: TestClient):
    data = {
        "text": "abra",
        "file_mask": "*.*",
        "size": {
            "value": 42000000,
            "operator": "le"
        },
        "creation_time": {
            "value": str(datetime.now()+timedelta(days=1)),
            "operator": "le"
        }
    }
    response = client.post("http://localhost/search", json=data)
    search_id = response.json()["search_id"]
    response = client.get(f"http://localhost/searches/{search_id}")

    assert response.status_code == 200
    assert ("finished" in response.json()) == True
    assert response.json()["finished"] == False

    time.sleep(5)

    response = client.get(f"http://localhost/searches/{search_id}")

    assert response.status_code == 200
    assert ("finished" in response.json()) == True
    assert response.json()["finished"] == True
    assert ("paths" in response.json()) == True
    assert len(response.json()["paths"]) == 1
    assert response.json()["paths"][0].endswith("test_dir\\test1.txt") == True


def test_health_check(client: TestClient):
    response = client.get("http://localhost/ping")

    assert response.status_code == 200
    assert response.json()['Result'] == "pong"

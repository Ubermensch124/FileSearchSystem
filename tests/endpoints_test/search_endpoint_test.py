import time

from fastapi.testclient import TestClient


class TestPost:
    @staticmethod
    def test_post_default(client: TestClient, data: dict):
        response = client.post("http://localhost/search", json=data["standard"])

        assert response.status_code == 201
        assert ("search_id" in response.json()) is True

    @staticmethod
    def test_post_double(client: TestClient, data: dict):
        response_first = client.post("http://localhost/search", json=data["standard"])
        response_second = client.post("http://localhost/search", json=data["standard"])

        assert response_first.status_code == 201
        assert response_second.status_code == 201
        assert ("search_id" in response_first.json()) is True
        assert ("search_id" in response_second.json()) is True
        assert response_first.json()["search_id"] != response_second.json()["search_id"]
        
    @staticmethod
    def test_post_bad(client: TestClient, data: dict):
        response = client.post("http://localhost/search", json=data["bad"])

        assert response.status_code >= 400


class TestGet:
    @staticmethod
    def test_get_default(client: TestClient, data: dict):
        id_from_post_request = client.post("http://localhost/search", json=data["standard"])
        search_id = id_from_post_request.json()["search_id"]

        response = client.get(f"http://localhost/searches/{search_id}")

        assert response.status_code == 200
        assert ("finished" in response.json()) is True
        assert response.json()["finished"] is False

        time.sleep(15)
        response = client.get(f"http://localhost/searches/{search_id}")

        assert response.status_code == 200
        assert ("finished" in response.json()) is True
        assert response.json()["finished"] is True
        assert ("paths" in response.json()) is True
        assert len(response.json()["paths"]) == 6

    @staticmethod
    def test_get_double(client: TestClient, data: dict):
        id_from_post_request_1 = client.post("http://localhost/search", json=data["standard"])
        id_from_post_request_2 = client.post("http://localhost/search", json=data["standard"])
        search_id_1 = id_from_post_request_1.json()["search_id"]
        search_id_2 = id_from_post_request_2.json()["search_id"]
        
        response_1 = client.get(f"http://localhost/searches/{search_id_1}")
        response_2 = client.get(f"http://localhost/searches/{search_id_2}")

        assert response_1.status_code == 200
        assert response_2.status_code == 200
        
        assert ("finished" in response_1.json()) is True
        assert response_1.json()["finished"] is False
        assert ("finished" in response_2.json()) is True
        assert response_2.json()["finished"] is False

        time.sleep(15)
        response_1 = client.get(f"http://localhost/searches/{search_id_1}")
        response_2 = client.get(f"http://localhost/searches/{search_id_2}")

        assert response_1.status_code == 200
        assert ("finished" in response_1.json()) is True
        assert response_1.json()["finished"] is True
        assert ("paths" in response_1.json()) is True
        assert len(response_1.json()["paths"]) == 6
        
        assert response_2.status_code == 200
        assert ("finished" in response_2.json()) is True
        assert response_2.json()["finished"] is True
        assert ("paths" in response_2.json()) is True
        assert len(response_2.json()["paths"]) == 6
    
    @staticmethod
    def test_get_bad(client: TestClient):
        bad_id = "this_is_bad_id"
        response = client.get(f"http://localhost/searches/{bad_id}")

        assert response.status_code >= 400

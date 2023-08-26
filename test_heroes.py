import requests
import json
import time

from requests import Response

BASE_URL = "http://localhost:5000"


def get_response(url: str) -> Response:
    start_time = time.time()

    url = BASE_URL + url
    print("")
    print(f"{url}:")
    response = requests.get(url)
    print(json.dumps(response.json(), indent=4))
    elapsed = time.time() - start_time
    
    print(f"Elapsed: {elapsed:.2f} sec.")

    return response


def test_get_heroes():
    response = get_response("/heroes/")
    assert response.status_code == 200


def test_get_hero(id: int = 1):
    response = get_response(f"/hero/{id}")
    assert response.status_code == 200


def test_get_teams():
    response = get_response("/teams/")
    assert response.status_code == 200


def test_get_team(id: int = 1):
    response = get_response(f"/team/{id}")
    assert response.status_code == 200


if __name__ == "__main__":
    test_get_heroes()
    test_get_hero(2)
    test_get_teams()
    test_get_team(2)

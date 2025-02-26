import pytest
import time
from flask import Flask, Response
from catbotsapi.app import app
from typing import Dict, List, Union


@pytest.fixture
def client() -> Flask:
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_ping(client: Flask) -> None:
    response: Response = client.get("/ping")
    assert response.status_code == 200
    assert response.data == b"Cats Service. Version 0.1"


def test_invalid_attribute(client: Flask) -> None:
    response: Response = client.get("/cats?attribute=invalid")
    assert response.status_code == 400
    assert response.json == {"error": "Invalid attribute"}


def test_invalid_order(client: Flask) -> None:
    response: Response = client.get("/cats?order=invalid")
    assert response.status_code == 400
    assert response.json == {"error": "Invalid order"}


def test_get_default_data_cats(client: Flask) -> None:
    response: Response = client.get("/cats")
    assert response.status_code == 200
    data: List[Dict[str, Union[str, int]]] = response.get_json()
    assert isinstance(data, list)
    assert len(data) <= 10


def test_add_duplicate_cat(client: Flask) -> None:
    new_cat: Dict[str, Union[str, int]] = {
        "name": "Tom",
        "color": "Gray",
        "tail_length": 30,
        "whiskers_length": 15,
    }
    client.post("/cat", json=new_cat)
    response = client.post("/cat", json=new_cat)
    assert response.status_code == 409
    assert response.get_json() == {"error": "Cat already exists"}


def test_add_invalid_cat_data(client: Flask) -> None:
    invalid_data: Dict[str, Union[str, int]] = {
        "name": "",
        "color": 123,
        "tail_length": -1,
        "whiskers_length": "long",
    }

    response: Response = client.post("/cat", json=invalid_data)
    assert response.status_code == 400
    assert "Color is invalid" in response.json["error"]
    assert "Tail_length is invalid" in response.json["error"]
    assert "Whiskers_length is invalid" in response.json["error"]


def test_rate_limit(client: Flask) -> None:
    for _ in range(600):
        response: Response = client.get("/cats")
        assert response.status_code == 200, f"Failed at request {_ + 1}"
        time.sleep(0.1)

    response: Response = client.get("/cats")
    assert response.status_code == 429, "Expected 429 Too Many Requests"
    assert response.get_json() == {"message": "Rate limit exceeded: 600 per 1 minute"}

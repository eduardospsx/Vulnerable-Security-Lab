import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_homepage(client):
    response = client.get("/")

    assert response.status_code == 200


def test_search(client):
    response = client.get("/search?q=hello")

    assert response.status_code == 200


def test_user_lookup(client):
    response = client.get("/user?username=admin")

    assert response.status_code == 200


def test_ping(client):
    response = client.get("/ping?host=127.0.0.1")

    assert response.status_code == 200


def test_hash_password():
    from app import hash_password

    result = hash_password("password123")

    assert len(result) == 32


def test_load_endpoint_requires_data(client):
    response = client.get("/load")

    assert response.status_code != 200
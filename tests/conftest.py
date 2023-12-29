import pytest

from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def test_clubs():
    return [
        {
            "name": "Test Club",
            "email": "testclubmail@example.co",
            "points": "10"
        }
    ]


@pytest.fixture
def mock_load_clubs():
    return [
        {
            "name": "Test Club",
            "email": "testclubmail@example.co",
            "points": "10"
        }
    ]


@pytest.fixture
def mock_load_competitions():
    return [
        {
            "name": "Test Competition",
            "date": "2023-01-01",
            "numberOfPlaces": "30"
        }
    ]

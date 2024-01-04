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
            "date": "2030-10-22 13:30:00",
            "numberOfPlaces": "30"
        }
    ]


class MockSaveFunction:
    # A mock class designed to simulate a save function. It stores the last argument passed to it, allowing tests to
    # verify if data was correctly passed to the mock function.
    def __init__(self):
        self.last_call_arg = None

    def __call__(self, data):
        self.last_call_arg = data


@pytest.fixture
def mock_save_clubs():
    # A mock class designed to simulate a save function. It stores the last argument passed to it, allowing tests to
    # verify if data was correctly passed to the mock function.
    return MockSaveFunction()


@pytest.fixture
def mock_save_competitions():
    # A pytest fixture that returns a mock save function specifically for competitions. This fixture is used to
    # simulate saving competition data in tests and to check the data passed to the save function.
    return MockSaveFunction()

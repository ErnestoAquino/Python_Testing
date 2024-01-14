import pytest

from server import app


@pytest.fixture
def client():
    # Set up a test client.
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_load_clubs():
    # Mocks the loadClubs function.
    return [
        {
            "name": "Test Club",
            "email": "testclubmail@example.co",
            "points": "10"
        }
    ]


@pytest.fixture
def mock_load_competitions():
    # Mocks the loadCompetitions function.
    return [
        {
            "name": "Test Competition",
            "date": "2030-10-22 13:30:00",
            "numberOfPlaces": "30"
        }
    ]


class MockSaveFunction:
    # A mock class designed to simulate a save function. It stores the last argument passed to it, allowing tests to
    # verify if data was correctly passed to the mock function. It can also simulate success or failure of the save
    # operation.
    def __init__(self, should_succeed=True):
        self.last_call_arg = None
        self.should_succeed = should_succeed

    def __call__(self, data):
        self.last_call_arg = data
        return self.should_succeed


@pytest.fixture
def mock_save_clubs():
    # Returns a mock save function for clubs.
    return MockSaveFunction(should_succeed=True)


@pytest.fixture
def mock_save_competitions():
    # Returns a mock save function for competitions.
    return MockSaveFunction(should_succeed=True)


@pytest.fixture
def mock_save_clubs_fail():
    # Returns a mock save function for clubs that simulates a failure in saving.
    return MockSaveFunction(should_succeed=False)


@pytest.fixture
def mock_save_competitions_fail():
    # Returns a mock save function for competitions that simulates a failure in saving.
    return MockSaveFunction(should_succeed=False)

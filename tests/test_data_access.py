import json
from data_access import loadClubs
from data_access import loadCompetitions
from data_access import save_clubs
from data_access import save_competitions


# -------------------------------------------------------
# Tests for loadClubs Function
# -------------------------------------------------------
def test_load_clubs_success(mocker):
    # Test: Verify successful loading of club data from a file.

    mock_clubs_data = {
        "clubs": [
            {"name": "Club A", "email": "cluba@example.com", "points": "100"},
            {"name": "Club B", "email": "clubb@example.com", "points": "200"}
        ]
    }

    # Mock for the file
    mocker.patch("builtins.open", mocker.mock_open(read_data=json.dumps(mock_clubs_data)))
    clubs = loadClubs()

    assert clubs == mock_clubs_data["clubs"]


def test_load_clubs_file_not_found_return_empty_list(mocker):
    # Test: Handle the situation where the club data file does not exist.

    mocker.patch("builtins.open", side_effect=FileNotFoundError)  # Simulate that the file does not exist
    expected_result = []  # Expected result
    clubs = loadClubs()

    assert clubs == expected_result  # Verify against the expected result


def test_load_clubs_json_decode_error_returns_empty_list(mocker):
    # Test: Handle invalid JSON content in the club data file.

    mocker.patch("builtins.open",
                 mocker.mock_open(read_data="This is not JSON"))  # Mock for a file with invalid content
    expected_result = []  # Expected result
    clubs = loadClubs()

    assert clubs == expected_result  # Verify against the expected result


# -------------------------------------------------------
# Tests for loadCompetitions Function
# -------------------------------------------------------
def test_load_competitions_success(mocker):
    # Test: Verify successful loading of competition data from a file.

    mock_competitions_data = {
        "competitions": [
            {"name": "Competition A", "date": "2030-10-22 13:30:00", "numberOfPlaces": "25"},
            {"name": "Competition B", "date": "2020-06-15 13:30:00", "numberOfPlaces": "30"}
        ]
    }

    # Mock for the file
    mocker.patch("builtins.open", mocker.mock_open(read_data=json.dumps(mock_competitions_data)))
    competitions = loadCompetitions()

    assert competitions == mock_competitions_data["competitions"]


def test_load_competitions_file_not_found_return_empty_list(mocker):
    # Test: Handle the situation where the competition data file does not exist.

    mocker.patch("builtins.open", side_effect=FileNotFoundError)  # Simulate that the file does not exist
    expected_result = []  # Expected result
    competitions = loadCompetitions()

    assert competitions == expected_result  # Verify against the expected result


def test_load_competitions_json_decode_error_return_empty_list(mocker):
    # Test: Handle invalid JSON content in the competition data file.

    mocker.patch("builtins.open",
                 mocker.mock_open(read_data="This is not JSON"))  # Mock for a file with invalid content
    expected_result = []  # Expected result
    competitions = loadCompetitions()

    assert competitions == expected_result  # Verify against the expected result


# -------------------------------------------------------
# Tests for save_clubs Function
# -------------------------------------------------------

def test_save_clubs_success(mocker):
    # Test: Verify successful saving of club data to a file.
    mock_clubs_data = {
        "clubs": [
            {"name": "Club A", "email": "cluba@example.com", "points": "100"},
            {"name": "Club B", "email": "clubb@example.com", "points": "200"}
        ]
    }
    mocker.patch("builtins.open", mocker.mock_open())
    expected_result = True
    result = save_clubs(mock_clubs_data)  # Call the function being tested

    assert result == expected_result  # Verify that the function returns True


def test_save_club_io_error(mocker):
    # Test: Handle an IOError when attempting to save club data.
    mock_clubs_data = {
        "clubs": [
            {"name": "Club A", "email": "cluba@example.com", "points": "100"},
            {"name": "Club B", "email": "clubb@example.com", "points": "200"}
        ]
    }

    mocker.patch("builtins.open", mocker.mock_open())  # Mock the open function to simulate file operations
    mocker.patch("json.dump", side_effect=IOError)  # Mock json.dump to throw an IOError, simulating a write error
    expected_result = False
    result = save_clubs(mock_clubs_data)

    # Asserting that the result is False (indicating failure)
    assert result == expected_result


# -------------------------------------------------------
# Tests for save_competitions Function
# -------------------------------------------------------

def test_save_competitions_success(mocker):
    # Test: Verify successful saving of competition data to a file.
    mock_competitions_data = {
        "competitions": [
            {"name": "Competition A", "date": "2030-10-22 13:30:00", "numberOfPlaces": "25"},
            {"name": "Competition B", "date": "2020-06-15 13:30:00", "numberOfPlaces": "30"}
        ]
    }
    mocker.patch("builtins.open", mocker.mock_open())
    expected_result = True
    result = save_competitions(mock_competitions_data)  # Call the function being tested

    assert result == expected_result  # Verify that the function returns True


def test_save_competitions_io_error(mocker):
    # Test: Handle an IOError when attempting to save competition data.
    mock_competitions_data = {
        "competitions": [
            {"name": "Competition A", "date": "2030-10-22 13:30:00", "numberOfPlaces": "25"},
            {"name": "Competition B", "date": "2020-06-15 13:30:00", "numberOfPlaces": "30"}
        ]
    }

    mocker.patch("builtins.open", mocker.mock_open())  # Mock the open function to simulate file operations
    mocker.patch("json.dump", side_effect=IOError)  # Mock json.dump to throw an IOError, simulating a write error
    expected_result = False
    result = save_competitions(mock_competitions_data)

    # Asserting that the result is False (indicating failure)
    assert result == expected_result

import json
from data_access import loadClubs
from data_access import loadCompetitions


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

    mocker.patch("builtins.open", side_effect=FileNotFoundError) # Simulate that the file does not exist
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


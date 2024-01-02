from datetime import datetime
from server import parse_competition_date
from server import is_competition_past


# -------------------------------------------------------
# Tests for parse_competition_date Function
# -------------------------------------------------------

def test_parse_valid_date():
    # Test: Parse a correctly formatted date string into a datetime object.
    # This test checks that a valid date string is successfully converted.
    valid_date = "2023-09-15 12:00:00"

    expected_date = datetime(2023, 9, 15, 12, 0, 0)
    assert parse_competition_date(valid_date) == expected_date


def test_parse_invalid_format_date():
    # Test: Attempt to parse a date string in an incorrect format.
    # This test checks that the function returns None when the date format is not as expected.
    invalid_format_date = "15/09/2023 12:00"

    assert parse_competition_date(invalid_format_date) is None


def test_parse_empty_string():
    # Test: Attempt to parse an empty string as a date.
    # This test checks that the function returns None when provided with an empty string.
    empty_date = ""

    assert parse_competition_date(empty_date) is None


def test_parse_invalid_date():
    # Test: Attempt to parse a string representing an invalid date (32/01/2023).
    # This test checks that the function returns None for non-existent dates.
    invalid_date = "2023-01-32 00:00:00"

    assert parse_competition_date(invalid_date) is None


def test_parse_non_date_string():
    # Test: Attempt to parse a string that is not a date at all.
    # This test checks that the function returns None when the input is not a date.
    no_date_string = "This is not a date"

    assert parse_competition_date(no_date_string) is None


# -------------------------------------------------------
# Tests for is_competition_past Function
# -------------------------------------------------------


def test_competition_date_passed():
    # Test: Check if the function correctly identifies a competition date that has already passed.
    competition_date = datetime(2024, 1, 2, 10, 00, 00)
    current_date = datetime(2024, 1, 3, 10, 00, 00)

    assert is_competition_past(competition_date, current_date) is True


def test_competition_date_future():
    # Test: Verify that the function correctly identifies a future competition date.
    competition_date = datetime(2024, 1, 3, 10, 00, 00)
    current_date = datetime(2024, 1, 2, 10, 00, 00)

    assert not is_competition_past(competition_date, current_date)


def test_competition_date_same():
    # Test: Determine if the function correctly handles the scenario
    # where the competition date and current date are the same.
    date = datetime(2024, 1, 2, 10, 00, 00)

    assert not is_competition_past(date, date)


def test_competition_same_day_different_hours():
    # Test: Check if the function accurately identifies a past competition date on the same day but at an earlier hour.
    competition_date = datetime(2024, 1, 2, 9, 00, 00)
    current_date = datetime(2024, 1, 2, 10, 00, 00)

    assert is_competition_past(competition_date, current_date)

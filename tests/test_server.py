from constants import EMAIL_NOT_FOUND_ERROR
from constants import EMAIL_EMPTY_ERROR
from constants import BOOKING_COMPLETE_MESSAGE
from constants import INSUFFICIENT_POINTS_MESSAGE
from constants import INSUFFICIENT_PLACES_MESSAGE
from constants import INVALID_PLACES_MESSAGE
from constants import NON_POSITIVE_PLACES_MESSAGE
from constants import INVALID_CLUB_OR_COMPETITION
from constants import MAX_PLACES_PER_BOOKING_MESSAGE
from constants import PAST_COMPETITION_BOOKING_ERROR_MESSAGE
from constants import INVALID_DATE_FORMAT_MESSAGE
from constants import LOADING_MESSAGE_ERROR
from constants import SAVE_CHANGES_MESSAGE_ERROR


# -------------------------------------------------------
# Tests for showSummary Function
# -------------------------------------------------------

def test_show_summary_with_valid_email(client, test_clubs, mocker):
    # Test: Show summary page with a valid email. The page should load successfully and display a welcome message.
    mocker.patch('server.loadClubs', return_value=test_clubs)
    valid_email = test_clubs[0]['email']
    print(valid_email)
    response = client.post('/showSummary', data={'email': valid_email})
    assert response.status_code == 200
    assert b'Welcome' in response.data


def test_show_summary_with_invalid_email(client):
    # Test: Attempt to show summary page with an invalid email. This should still return a 200 status code but show
    # an email not found error.
    invalid_email = "noexistingemail@example.com"
    response = client.post('/showSummary', data={'email': invalid_email}, follow_redirects=True)
    assert response.status_code == 200
    assert EMAIL_NOT_FOUND_ERROR.encode() in response.data


def test_show_summary_with_empty_email(client):
    # Test: Attempt to show summary page with an empty email field. This should return a 200 status code and show an
    # error for empty email.
    response = client.post('/showSummary', data={'email': ''}, follow_redirects=True)
    assert response.status_code == 200
    assert EMAIL_EMPTY_ERROR.encode() in response.data


def test_show_summary_with_loading_error(client, mocker, test_clubs):
    # Test: Simulate an error in loading clubs or competitions data. This should show a loading error message.
    mocker.patch('server.loadClubs', return_value=[])  # Simulates that the loading of clubs data fails
    mocker.patch('server.loadCompetitions', return_value=[])  # Simulates that the loading of competitions data fails
    valid_email = test_clubs[0]['email']

    response = client.post('/showSummary', data={'email': valid_email}, follow_redirects=True)

    assert response.status_code == 200
    assert LOADING_MESSAGE_ERROR.encode() in response.data


# -------------------------------------------------------
# Tests for purchasePlaces Function
# -------------------------------------------------------

def test_purchase_places_valid_and_confirmation_message(client, mocker, mock_load_clubs, mock_load_competitions):
    # Test: Validate successful purchase of places for a competition.
    mocker.patch('server.loadClubs', return_value=mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value=mock_load_competitions)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    response = client.post('/purchasePlaces', data={
        'competition': "Test Competition",
        'club': "Test Club",
        'places': "5"
    })
    expected_confirmation_message = "You have reserved 5 place(s) for the competition Test Competition."

    assert response.status_code == 200
    assert BOOKING_COMPLETE_MESSAGE.encode() in response.data

    # Check for the presence of the booking confirmation message
    assert expected_confirmation_message.encode() in response.data


def test_purchase_places_with_insufficient_points(client, mocker, mock_load_competitions):
    # Test: Attempt to purchase places in a competition with a club that has insufficient points.
    insufficient_points_club = [
        {
            "name": "Test Club",
            "email": "testclubmail@example.co",
            "points": "3"  # Insufficient points for the purchase
        }
    ]

    mocker.patch('server.loadClubs', return_value=insufficient_points_club)
    mocker.patch('server.loadCompetitions', return_value=mock_load_competitions)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    response = client.post('/purchasePlaces', data={
        'competition': "Test Competition",
        'club': "Test Club",
        'places': "5"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert INSUFFICIENT_POINTS_MESSAGE.encode() in response.data


def test_purchase_places_when_insufficient_places(client, mocker, mock_load_clubs):
    # Test: Attempt to purchase more places in a competition than are available.
    insufficient_places_competitions = [
        {
            "name": "Test Competition",
            "date": "2050-10-22 13:30:00",
            "numberOfPlaces": "2"  # Insufficient places for purchase
        }
    ]

    mocker.patch('server.loadClubs', return_value=mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value=insufficient_places_competitions)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    response = client.post('/purchasePlaces', data={
        'competition': "Test Competition",
        'club': "Test Club",
        'places': "5"  # More places than are available
    }, follow_redirects=True)

    assert response.status_code == 200
    assert INSUFFICIENT_PLACES_MESSAGE.encode() in response.data


def test_purchase_places_invalid_number_of_places(client, mocker, mock_load_clubs, mock_load_competitions):
    # Test: Attempt to purchase places in a competition with an invalid number format for the requested places.
    mocker.patch('server.loadClubs', return_value=mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value=mock_load_competitions)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    invalid_places = "invalid"  # Invalid value for the number of places

    response = client.post('/purchasePlaces', data={
        'competition': "Test Competition",
        'club': "Test Club",
        'places': invalid_places
    }, follow_redirects=True)

    assert response.status_code == 200
    assert INVALID_PLACES_MESSAGE.encode() in response.data


def test_purchase_places_zero_places(client, mocker, mock_load_clubs, mock_load_competitions):
    # Test: Attempt to purchase zero places in a competition.
    mocker.patch('server.loadClubs', return_value=mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value=mock_load_competitions)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    response = client.post('/purchasePlaces', data={
        'competition': "Test Competition",
        'club': "Test Club",
        'places': "0"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert NON_POSITIVE_PLACES_MESSAGE.encode() in response.data


def test_purchase_places_negative_places(client, mocker, mock_load_clubs, mock_load_competitions):
    # Test: Attempt to purchase a negative number of places in a competition.
    mocker.patch('server.loadClubs', return_value=mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value=mock_load_competitions)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    response = client.post('/purchasePlaces', data={
        'competition': "Test Competition",
        'club': "Test Club",
        'places': "-1"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert NON_POSITIVE_PLACES_MESSAGE.encode() in response.data


def test_purchase_places_no_club_found(client, mocker, mock_load_clubs, mock_load_competitions):
    # Test: Attempt to purchase places with a club that does not exist.
    mocker.patch('server.loadClubs', return_value=mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value=mock_load_competitions)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    response = client.post('/purchasePlaces', data={
        'competition': "Test Competition",
        'club': "Nonexistent Club",
        'places': "5"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert INVALID_CLUB_OR_COMPETITION.encode() in response.data


def test_purchase_places_no_competition_found(client, mocker, mock_load_clubs, mock_load_competitions):
    # Test: Attempt to purchase places for a competition that does not exist.
    mocker.patch('server.loadClubs', return_value=mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value=mock_load_competitions)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    response = client.post('/purchasePlaces', data={
        'competition': "Nonexistent Competition",
        'club': "Test Club",
        'places': "5"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert INVALID_CLUB_OR_COMPETITION.encode() in response.data


def test_purchase_places_exceeding_place_limit(client, mocker, mock_load_clubs, mock_load_competitions):
    # Test: Attempt to purchase more than 12 places in a competition.
    mocker.patch('server.loadClubs', return_value=mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value=mock_load_competitions)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    response = client.post('/purchasePlaces', data={
        'competition': "Test Competition",
        'club': "Test Club",
        'places': "13"  # Attempting to book more than 12 places
    }, follow_redirects=True)

    assert response.status_code == 200
    assert MAX_PLACES_PER_BOOKING_MESSAGE.encode() in response.data


def test_purchase_places_with_future_competition(client, mocker, mock_load_clubs):
    # Test: Attempt to purchase places for a competition set in the future.
    future_competition = [
        {
            "name": "Test Competition",
            "date": "2100-10-22 13:30:00",  # Future date
            "numberOfPlaces": "20"
        }
    ]
    mocker.patch('server.loadClubs', return_value=mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value=future_competition)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    response = client.post('/purchasePlaces', data={
        'competition': "Test Competition",
        'club': "Test Club",
        'places': "1"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert BOOKING_COMPLETE_MESSAGE.encode() in response.data


def test_purchase_places_with_past_competition(client, mocker, mock_load_clubs):
    # Test: Attempt to purchase places for a competition that has already occurred in the past.
    past_competition = [
        {
            "name": "Test Competition",
            "date": "2000-10-22 13:30:00",  # Past date
            "numberOfPlaces": "20"
        }
    ]
    mocker.patch('server.loadClubs', return_value=mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value=past_competition)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    response = client.post('/purchasePlaces', data={
        'competition': "Test Competition",
        'club': "Test Club",
        'places': "1"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert PAST_COMPETITION_BOOKING_ERROR_MESSAGE.encode() in response.data


def test_purchase_places_with_invalid_competition_date_format(client, mocker, mock_load_clubs):
    # Test: Attempt to purchase places for a competition with an invalid date format.
    invalid_format_competition = [
        {
            "name": "Test Competition",
            "date": "this is not a date",  # Invalid format
            "numberOfPlaces": "20"
        }
    ]
    mocker.patch('server.loadClubs', return_value=mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value=invalid_format_competition)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    response = client.post('/purchasePlaces', data={
        'competition': "Test Competition",
        'club': "Test Club",
        'places': "1"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert INVALID_DATE_FORMAT_MESSAGE.encode() in response.data


# -------------------------------------------------------
# Tests for purchasePlaces Function: Bug point update fix
# -------------------------------------------------------


def test_correct_point_deduction(client, mocker, mock_save_clubs, mock_save_competitions):
    # Test: Verify correct point deduction after a club purchases places in a competition.

    initial_points = 15  # Initial points of the club
    places_to_purchase = 5  # Number of places to purchase
    expected_points_after_purchase = initial_points - places_to_purchase  # Expected points after purchase

    mock_club = [
        {
            "name": "Test Club",
            "email": "testclubmail@example.co",
            "points": str(initial_points)  # Convert to string to simulate input data
        }
    ]

    mock_competition = [
        {
            "name": "Test Competition",
            "date": "2050-10-22 13:30:00",
            "numberOfPlaces": "20"
        }
    ]
    mocker.patch('server.loadClubs', return_value=mock_club)
    mocker.patch('server.loadCompetitions', return_value=mock_competition)
    mocker.patch('server.save_clubs', mock_save_clubs)
    mocker.patch('server.save_competitions', mock_save_competitions)

    # Perform the POST request
    response = client.post('/purchasePlaces', data={
        'competition': "Test Competition",
        'club': "Test Club",
        'places': str(places_to_purchase)
    })

    # Verify results
    assert response.status_code == 200
    assert BOOKING_COMPLETE_MESSAGE.encode() in response.data

    # Check that save_clubs was called with the updated points
    assert mock_save_clubs.last_call_arg[0]['points'] == str(expected_points_after_purchase)


def test_no_point_deduction_for_invalid_purchase(client, mocker, mock_save_clubs, mock_save_competitions):
    # Test: Ensure that no points are deducted from a club's total for an invalid purchase attempt
    # due to insufficient points

    initial_points = 3  # Initial points of the club, not enough for purchase
    places_to_purchase = 5  # Number of places to attempt to purchase

    mock_club = [
        {
            "name": "Test Club",
            "email": "testclubmail@example.co",
            "points": str(initial_points)  # Convert to string to simulate input data
        }
    ]
    mock_competition = [
        {
            "name": "Test Competition",
            "date": "2050-10-22 13:30:00",
            "numberOfPlaces": "20"
        }
    ]
    mocker.patch('server.loadClubs', return_value=mock_club)
    mocker.patch('server.loadCompetitions', return_value=mock_competition)
    mocker.patch('server.save_clubs', mock_save_clubs)
    mocker.patch('server.save_competitions', mock_save_competitions)

    # Perform the POST request
    response = client.post('/purchasePlaces', data={
        'competition': "Test Competition",
        'club': "Test Club",
        'places': str(places_to_purchase)
    }, follow_redirects=True)

    # Verify results
    assert response.status_code == 200
    assert INSUFFICIENT_POINTS_MESSAGE.encode() in response.data

    # Verify that the save_club function was not called to ensure that the club's points were not modified
    assert mock_save_clubs.last_call_arg is None


def test_point_deduction_for_max_place_purchase(client, mocker, mock_save_clubs, mock_save_competitions):
    initial_points = 20
    max_places_to_purchase = 12
    expected_points_after_purchase = initial_points - max_places_to_purchase

    mock_club = [
        {
            "name": "Test Club",
            "email": "testclubmail@example.co",
            "points": str(initial_points)  # Convert to string to simulate input data
        }
    ]

    mock_competition = [
        {
            "name": "Test Competition",
            "date": "2050-10-22 13:30:00",
            "numberOfPlaces": "30"  # Sufficient availability of places
        }
    ]

    mocker.patch('server.loadClubs', return_value=mock_club)
    mocker.patch('server.loadCompetitions', return_value=mock_competition)
    mocker.patch('server.save_clubs', mock_save_clubs)
    mocker.patch('server.save_competitions', mock_save_competitions)

    # Perform the POST request to purchase the maximum number of places
    response = client.post('/purchasePlaces', data={
        'competition': "Test Competition",
        'club': "Test Club",
        'places': str(max_places_to_purchase)
    }, follow_redirects=True)

    # Verify results
    assert response.status_code == 200
    assert BOOKING_COMPLETE_MESSAGE.encode() in response.data

    # Verify that save_clubs was called with the updated points
    assert mock_save_clubs.last_call_arg[0]['points'] == str(expected_points_after_purchase)


def test_save_error_handling_places(client, mocker, mock_save_clubs_fail, mock_save_competitions_fail):
    #  Test: Verify the server's error handling when there's a failure in saving changes after a purchase.

    mock_competition = [
        {
            "name": "Test Competition",
            "date": "2100-10-22 13:30:00",
            "numberOfPlaces": "15"
        }
    ]

    mock_club = [
        {
            "name": "Test Club",
            "email": "testclubmail@example.co",
            "points": "20"
        }
    ]

    mocker.patch('server.loadClubs', return_value=mock_club)
    mocker.patch('server.loadCompetitions', return_value=mock_competition)
    mocker.patch('server.save_clubs', mock_save_clubs_fail)
    mocker.patch('server.save_competitions', mock_save_competitions_fail)

    response = client.post('/purchasePlaces', data={
        'competition': "Test Competition",
        'club': "Test Club",
        'places': "5"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert SAVE_CHANGES_MESSAGE_ERROR.encode() in response.data

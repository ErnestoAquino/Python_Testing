import server
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
from constants import COMPETITION_FULL_MESSAGE
from constants import ERROR_MESSAGE_RETRY
from constants import INVALID_POINTS_MESSAGE
# -------------------------------------------------------
# Tests for flow
# -------------------------------------------------------
def test_integration_flow(client, mocker, mock_load_clubs, mock_load_competitions, mock_save_clubs,
                          mock_save_competitions):
    # Test: This integration test simulates a complete user journey through the web application. It includes visiting
    # the home page, displaying the summary page for a club, booking places in a competition, completing a purchase,
    # and finally logging out. This test ensures that each step in the flow works as expected and the system responds
    # correctly at each stage.

    existing_mail = "testclubmail@example.co"
    existing_club = "Test Club"
    existing_competition = "Test Competition"
    expected_confirmation_message = "You have reserved 5 place(s) for the competition Test Competition."

    # Mock the loadsClubs y loadCompetitions functions
    mocker.patch('server.loadClubs', return_value = mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value = mock_load_competitions)
    mocker.patch('server.save_clubs', mock_save_clubs)
    mocker.patch('server.save_competitions', mock_save_competitions)

    # index: GET request to the root route
    response = client.get('/')
    assert response.status_code == 200

    # showSummary: POST request
    response = client.post('/showSummary', data = {'email': existing_mail})
    assert response.status_code == 200

    # book: GET request to the booking route for a specific club and competition
    response = client.get(f'/book/{existing_competition}/{existing_club}')
    assert response.status_code == 200

    # purchasePlaces: POST request to make a purchase
    response = client.post('/purchasePlaces', data = {
        'competition': "Test Competition",
        'club': "Test Club",
        'places': "5"
    })

    assert response.status_code == 200
    assert BOOKING_COMPLETE_MESSAGE.encode() in response.data
    assert expected_confirmation_message.encode() in response.data

    # logout: GET request to the logout route
    response = client.get('/logout', follow_redirects = True)
    assert response.status_code == 200
    assert b'Welcome' in response.data


# -------------------------------------------------------
# Tests for showSummary Function
# -------------------------------------------------------

def test_show_summary_with_valid_email(client, test_clubs, mocker):
    # Test: Show summary page with a valid email. The page should load successfully and display a welcome message.
    mocker.patch('server.loadClubs', return_value = test_clubs)
    valid_email = test_clubs[0]['email']
    print(valid_email)
    response = client.post('/showSummary', data = {'email': valid_email})
    assert response.status_code == 200
    assert b'Welcome' in response.data


def test_show_summary_with_invalid_email(client):
    # Test: Attempt to show summary page with an invalid email. This should still return a 200 status code but show
    # an email not found error.
    invalid_email = "noexistingemail@example.com"
    response = client.post('/showSummary', data = {'email': invalid_email}, follow_redirects = True)
    assert response.status_code == 200
    assert EMAIL_NOT_FOUND_ERROR.encode() in response.data


def test_show_summary_with_empty_email(client):
    # Test: Attempt to show summary page with an empty email field. This should return a 200 status code and show an
    # error for empty email.
    response = client.post('/showSummary', data = {'email': ''}, follow_redirects = True)
    assert response.status_code == 200
    assert EMAIL_EMPTY_ERROR.encode() in response.data


def test_show_summary_with_loading_error(client, mocker, test_clubs):
    # Test: Simulate an error in loading clubs or competitions data. This should show a loading error message.
    mocker.patch('server.loadClubs', return_value = [])  # Simulates that the loading of clubs data fails
    mocker.patch('server.loadCompetitions', return_value = [])  # Simulates that the loading of competitions data fails
    valid_email = test_clubs[0]['email']

    response = client.post('/showSummary', data = {'email': valid_email}, follow_redirects = True)

    assert response.status_code == 200
    assert LOADING_MESSAGE_ERROR.encode() in response.data


# -------------------------------------------------------
# Tests for purchasePlaces Function
# -------------------------------------------------------

def test_purchase_places_valid_and_confirmation_message(client, mocker, mock_load_clubs, mock_load_competitions):
    # Test: Validate successful purchase of places for a competition.
    mocker.patch('server.loadClubs', return_value = mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value = mock_load_competitions)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    response = client.post('/purchasePlaces', data = {
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

    mocker.patch('server.loadClubs', return_value = insufficient_points_club)
    mocker.patch('server.loadCompetitions', return_value = mock_load_competitions)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    response = client.post('/purchasePlaces', data = {
        'competition': "Test Competition",
        'club': "Test Club",
        'places': "5"
    }, follow_redirects = True)

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

    mocker.patch('server.loadClubs', return_value = mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value = insufficient_places_competitions)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    response = client.post('/purchasePlaces', data = {
        'competition': "Test Competition",
        'club': "Test Club",
        'places': "5"  # More places than are available
    }, follow_redirects = True)

    assert response.status_code == 200
    assert INSUFFICIENT_PLACES_MESSAGE.encode() in response.data


def test_purchase_places_invalid_number_of_places(client, mocker, mock_load_clubs, mock_load_competitions):
    # Test: Attempt to purchase places in a competition with an invalid number format for the requested places.
    mocker.patch('server.loadClubs', return_value = mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value = mock_load_competitions)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    invalid_places = "invalid"  # Invalid value for the number of places

    response = client.post('/purchasePlaces', data = {
        'competition': "Test Competition",
        'club': "Test Club",
        'places': invalid_places
    }, follow_redirects = True)

    assert response.status_code == 200
    assert INVALID_PLACES_MESSAGE.encode() in response.data


def test_purchase_places_zero_places(client, mocker, mock_load_clubs, mock_load_competitions):
    # Test: Attempt to purchase zero places in a competition.
    mocker.patch('server.loadClubs', return_value = mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value = mock_load_competitions)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    response = client.post('/purchasePlaces', data = {
        'competition': "Test Competition",
        'club': "Test Club",
        'places': "0"
    }, follow_redirects = True)

    assert response.status_code == 200
    assert NON_POSITIVE_PLACES_MESSAGE.encode() in response.data


def test_purchase_places_negative_places(client, mocker, mock_load_clubs, mock_load_competitions):
    # Test: Attempt to purchase a negative number of places in a competition.
    mocker.patch('server.loadClubs', return_value = mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value = mock_load_competitions)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    response = client.post('/purchasePlaces', data = {
        'competition': "Test Competition",
        'club': "Test Club",
        'places': "-1"
    }, follow_redirects = True)

    assert response.status_code == 200
    assert NON_POSITIVE_PLACES_MESSAGE.encode() in response.data


def test_purchase_places_no_club_found(client, mocker, mock_load_clubs, mock_load_competitions):
    # Test: Attempt to purchase places with a club that does not exist.
    mocker.patch('server.loadClubs', return_value = mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value = mock_load_competitions)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    response = client.post('/purchasePlaces', data = {
        'competition': "Test Competition",
        'club': "Nonexistent Club",
        'places': "5"
    }, follow_redirects = True)

    assert response.status_code == 200
    assert INVALID_CLUB_OR_COMPETITION.encode() in response.data


def test_purchase_places_no_competition_found(client, mocker, mock_load_clubs, mock_load_competitions):
    # Test: Attempt to purchase places for a competition that does not exist.
    mocker.patch('server.loadClubs', return_value = mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value = mock_load_competitions)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    response = client.post('/purchasePlaces', data = {
        'competition': "Nonexistent Competition",
        'club': "Test Club",
        'places': "5"
    }, follow_redirects = True)

    assert response.status_code == 200
    assert INVALID_CLUB_OR_COMPETITION.encode() in response.data


def test_purchase_places_exceeding_place_limit(client, mocker, mock_load_clubs, mock_load_competitions):
    # Test: Attempt to purchase more than 12 places in a competition.
    mocker.patch('server.loadClubs', return_value = mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value = mock_load_competitions)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    response = client.post('/purchasePlaces', data = {
        'competition': "Test Competition",
        'club': "Test Club",
        'places': "13"  # Attempting to book more than 12 places
    }, follow_redirects = True)

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
    mocker.patch('server.loadClubs', return_value = mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value = future_competition)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    response = client.post('/purchasePlaces', data = {
        'competition': "Test Competition",
        'club': "Test Club",
        'places': "1"
    }, follow_redirects = True)

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
    mocker.patch('server.loadClubs', return_value = mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value = past_competition)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    response = client.post('/purchasePlaces', data = {
        'competition': "Test Competition",
        'club': "Test Club",
        'places': "1"
    }, follow_redirects = True)

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
    mocker.patch('server.loadClubs', return_value = mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value = invalid_format_competition)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    response = client.post('/purchasePlaces', data = {
        'competition': "Test Competition",
        'club': "Test Club",
        'places': "1"
    }, follow_redirects = True)

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
    mocker.patch('server.loadClubs', return_value = mock_club)
    mocker.patch('server.loadCompetitions', return_value = mock_competition)
    mocker.patch('server.save_clubs', mock_save_clubs)
    mocker.patch('server.save_competitions', mock_save_competitions)

    # Perform the POST request
    response = client.post('/purchasePlaces', data = {
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
    mocker.patch('server.loadClubs', return_value = mock_club)
    mocker.patch('server.loadCompetitions', return_value = mock_competition)
    mocker.patch('server.save_clubs', mock_save_clubs)
    mocker.patch('server.save_competitions', mock_save_competitions)

    # Perform the POST request
    response = client.post('/purchasePlaces', data = {
        'competition': "Test Competition",
        'club': "Test Club",
        'places': str(places_to_purchase)
    }, follow_redirects = True)

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

    mocker.patch('server.loadClubs', return_value = mock_club)
    mocker.patch('server.loadCompetitions', return_value = mock_competition)
    mocker.patch('server.save_clubs', mock_save_clubs)
    mocker.patch('server.save_competitions', mock_save_competitions)

    # Perform the POST request to purchase the maximum number of places
    response = client.post('/purchasePlaces', data = {
        'competition': "Test Competition",
        'club': "Test Club",
        'places': str(max_places_to_purchase)
    }, follow_redirects = True)

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

    mocker.patch('server.loadClubs', return_value = mock_club)
    mocker.patch('server.loadCompetitions', return_value = mock_competition)
    mocker.patch('server.save_clubs', mock_save_clubs_fail)
    mocker.patch('server.save_competitions', mock_save_competitions_fail)

    response = client.post('/purchasePlaces', data = {
        'competition': "Test Competition",
        'club': "Test Club",
        'places': "5"
    }, follow_redirects = True)

    assert response.status_code == 200
    assert SAVE_CHANGES_MESSAGE_ERROR.encode() in response.data


def test_purchase_places_competition_full(client, mocker, mock_load_clubs):
    # Test: Attempt to purchase places in a competition that is already full.

    # Setting up a full competition
    full_competition = [
        {
            "name": "Full Competition",
            "date": "2050-10-22 13:30:00",
            "numberOfPlaces": "0"  # No places available
        }
    ]

    mocker.patch('server.loadClubs', return_value = mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value = full_competition)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    # Perform POST request to try purchasing places in the full competition
    response = client.post('/purchasePlaces', data = {
        "competition": "Full Competition",
        "club": "Test Club",
        "places": "1"
    }, follow_redirects = True)

    # Verify the results
    assert response.status_code == 200
    assert COMPETITION_FULL_MESSAGE.encode() in response.data


def test_load_error_handling(client, mocker):
    # Simulate loading error by returning empty lists
    mocker.patch('server.loadClubs', return_value = [])
    mocker.patch('server.loadCompetitions', return_value = [])

    # Perform a POST request that would normally trigger the loading
    response = client.post('/purchasePlaces', data = {
        "competition": "Some Competition",
        "club": "Some Club",
        "places": "1"
    }, follow_redirects = True)

    # Verify that the user is redirected to the index page
    assert response.status_code == 200
    assert LOADING_MESSAGE_ERROR.encode() in response.data


def test_invalid_points_handling(client, mocker, mock_save_clubs, mock_save_competitions):
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
            "points": "invalid_points_value"  # Invalid points
        }
    ]

    mocker.patch('server.loadClubs', return_value = mock_club)
    mocker.patch('server.loadCompetitions', return_value = mock_competition)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    response = client.post('/purchasePlaces', data = {
        'competition': "Test Competition",
        'club': "Test Club",
        'places': "5"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert INVALID_POINTS_MESSAGE.encode() in response.data


def test_invalid_places_handling(client, mocker, mock_save_clubs, mock_save_competitions):
    mock_competition = [
        {
            "name": "Test Competition",
            "date": "2100-10-22 13:30:00",
            "numberOfPlaces": "invalid_places_value"  # Invalid places
        }
    ]

    mock_club = [
        {
            "name": "Test Club",
            "email": "testclubmail@example.co",
            "points": "30"
        }
    ]

    mocker.patch('server.loadClubs', return_value = mock_club)
    mocker.patch('server.loadCompetitions', return_value = mock_competition)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    response = client.post('/purchasePlaces', data = {
        'competition': "Test Competition",
        'club': "Test Club",
        'places': "5"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert "Invalid number of places".encode() in response.data


# -------------------------------------------------------
# Tests for club_points Function
# -------------------------------------------------------


def test_club_points_page_loads(client, mocker, test_clubs):
    # Test: Verify that the club points page loads successfully.
    mocker.patch('server.loadClubs', return_value = test_clubs)
    response = client.get('/club-points')

    assert response.status_code == 200
    assert b"Club Points" in response.data


def test_club_points_display(client, mocker, test_clubs):
    # Test: Verify that the club points are correctly displayed on the page.
    mocker.patch('server.loadClubs', return_value = test_clubs)
    response = client.get('/club-points')
    for club in test_clubs:
        assert club['name'].encode() in response.data
        assert club['points'].encode() in response.data


def test_club_points_page_loading_error(client, mocker):
    # Test: Simulate a loading error and verify that an error message is displayed.
    mocker.patch('server.loadClubs', return_value = [])  # Simulate a loading error.
    response = client.get('/club-points', follow_redirects = True)
    assert response.status_code == 200
    assert LOADING_MESSAGE_ERROR.encode() in response.data


# -------------------------------------------------------
# Test for logout Function
# -------------------------------------------------------

def test_logout(client):
    # Test: Verify the logout route redirects to the index
    response = client.get('/logout', follow_redirects = True)

    assert response.status_code == 200
    assert b'Welcome' in response.data


# -------------------------------------------------------
# Test for book Function
# -------------------------------------------------------
def test_book_club_and_competition_found(client, mocker, mock_load_clubs, mock_load_competitions):
    # Test:Verify that booking page loads successfully when both club and competition are found.

    # Use existing club and competition names
    existing_club_name = "Test Club"
    existing_competition_name = "Test Competition"

    mocker.patch('server.loadClubs', return_value = mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value = mock_load_competitions)

    # Attempt to book for an existing club and competition.
    response = client.get(f'/book/{existing_competition_name}/{existing_club_name}')

    assert response.status_code == 200
    assert existing_competition_name.encode() in response.data  # Verify that the competition name is in the response
    assert b'How many places?' in response.data


def test_book_club_or_competition_not_found(client, mocker, mock_load_clubs, mock_load_competitions):
    # Test: Verify that booking fails and redirects with an error when club or competition is not found.

    nonexisting_club_name = "Non Existing Competition"
    nonexisting_competition_name = "Non Existing Competition"

    mocker.patch('server.loadClubs', return_value = mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value = mock_load_competitions)

    # Attempt to book for a club and competition that do not exist in the mock data.
    response = client.get(f'/book/{nonexisting_club_name}/{nonexisting_club_name}', follow_redirects = True)

    # Check that the response is a redirect to the welcome page with an error message.
    assert response.status_code == 200
    assert ERROR_MESSAGE_RETRY.encode() in response.data

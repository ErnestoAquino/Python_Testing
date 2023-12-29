from constants import EMAIL_NOT_FOUND_ERROR
from constants import EMAIL_EMPTY_ERROR
from constants import BOOKING_COMPLETE_MESSAGE
from constants import INSUFFICIENT_POINTS_MESSAGE
from constants import INSUFFICIENT_PLACES_MESSAGE
from constants import INVALID_PLACES_MESSAGE


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


# -------------------------------------------------------
# Tests for purchasePlaces Function
# -------------------------------------------------------

def test_purchase_places_valid(client, mocker, mock_load_clubs, mock_load_competitions):
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

    assert response.status_code == 200
    assert BOOKING_COMPLETE_MESSAGE.encode() in response.data


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
            "date": "2023-01-01",
            "numberOfPlaces": "2"  # Insufficient places for purchase
        }
    ]

    mocker.patch('server.loadClubs', return_value = mock_load_clubs)
    mocker.patch('server.loadCompetitions', return_value = insufficient_places_competitions)
    mocker.patch('server.save_clubs')
    mocker.patch('server.save_competitions')

    response = client.post('/purchasePlaces', data={
        'competition': "Test Competition",
        'club': "Test Club",
        'places': "5"  # More places than are available
    }, follow_redirects = True)

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
    }, follow_redirects = True)

    assert response.status_code == 200
    assert INVALID_PLACES_MESSAGE.encode() in response.data

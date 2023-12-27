import pytest

from constants import EMAIL_NOT_FOUND_ERROR
from constants import EMAIL_EMPTY_ERROR


def test_show_summary_with_valid_email(client, test_clubs, mocker):
    mocker.patch('server.loadClubs', return_value=test_clubs)
    valid_email = test_clubs[0]['email']
    print(valid_email)
    response = client.post('/showSummary', data={'email': valid_email})
    assert response.status_code == 200
    assert b'Welcome' in response.data


def test_show_summary_with_invalid_email(client):
    invalid_email = "noexistingemail@example.com"
    response = client.post('/showSummary', data={'email': invalid_email}, follow_redirects=True)
    assert response.status_code == 200
    assert EMAIL_NOT_FOUND_ERROR.encode() in response.data


def test_show_summary_with_empty_email(client):
    response = client.post('/showSummary', data={'email': ''}, follow_redirects=True)
    assert response.status_code == 200
    assert EMAIL_EMPTY_ERROR.encode() in response.data

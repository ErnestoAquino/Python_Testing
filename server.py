from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime

from constants import EMAIL_NOT_FOUND_ERROR
from constants import EMAIL_EMPTY_ERROR
from constants import INSUFFICIENT_PLACES_MESSAGE
from constants import INSUFFICIENT_POINTS_MESSAGE
from constants import BOOKING_COMPLETE_MESSAGE
from constants import INVALID_PLACES_MESSAGE
from constants import NON_POSITIVE_PLACES_MESSAGE
from constants import INVALID_POINTS_MESSAGE
from constants import INVALID_CLUB_OR_COMPETITION
from constants import MAX_PLACES_PER_BOOKING_MESSAGE
from constants import INVALID_DATE_FORMAT_MESSAGE
from constants import PAST_COMPETITION_BOOKING_ERROR_MESSAGE
from constants import LOADING_MESSAGE_ERROR
from constants import SAVE_CHANGES_MESSAGE_ERROR
from constants import COMPETITION_FULL_MESSAGE
from constants import ERROR_MESSAGE_RETRY

from utils import parse_competition_date
from utils import is_competition_past
from utils import purchase_limit

from data_access import load_clubs
from data_access import load_competitions
from data_access import save_clubs
from data_access import save_competitions

app = Flask(__name__)
app.secret_key = 'something_special'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/show-summary', methods=['POST'])
def show_summary():
    email = request.form.get('email')
    clubs = load_clubs()
    competitions = load_competitions()

    # Verify if the clubs and competitions data were loaded correctly
    if not clubs or not competitions:
        flash(LOADING_MESSAGE_ERROR)
        return redirect(url_for('index'))

    # Verify if an email has been provided
    if not email:
        flash(EMAIL_EMPTY_ERROR)
        return redirect(url_for('index'))

    # Search for the club corresponding to the provided email
    club = next((c for c in clubs if c['email'] == email), None)
    if not club:
        flash(EMAIL_NOT_FOUND_ERROR)
        return redirect(url_for('index'))
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    clubs = load_clubs()
    competitions = load_competitions()

    # Search for the corresponding competition and club
    found_club = next((c for c in clubs if c['name'] == club), None)
    found_competition = next((c for c in competitions if c['name'] == competition), None)

    if found_club and found_competition:
        return render_template('booking.html', club=found_club, competition=found_competition)
    else:
        flash(ERROR_MESSAGE_RETRY)
        return render_template('welcome.html', club=club, competition=competitions)


@app.route('/purchase-places', methods=['POST'])
def purchase_places():
    clubs = load_clubs()
    competitions = load_competitions()

    # Verify if the clubs and competitions were loaded correctly.
    if not clubs or not competitions:
        flash(LOADING_MESSAGE_ERROR)
        return redirect(url_for('index'))

    # Get the data form the form.
    competition_name = request.form.get('competition')
    club_name = request.form.get('club')

    # Search for the corresponding competition and club.
    selected_competition = next((c for c in competitions if c['name'] == competition_name), None)
    selected_club = next((c for c in clubs if c['name'] == club_name), None)

    # Check if the competition and club were found.
    if not selected_competition or not selected_club:
        flash(INVALID_CLUB_OR_COMPETITION)
        return redirect(url_for('index'))

    # Parse the competition date
    competition_date = parse_competition_date(selected_competition['date'])
    if competition_date is None:
        flash(INVALID_DATE_FORMAT_MESSAGE)
        return redirect(url_for('book', competition=selected_competition['name'], club=selected_club['name']))

    # Get current date
    current_date = datetime.now()

    # Check if the competition has already passed.
    if is_competition_past(competition_date, current_date):
        flash(PAST_COMPETITION_BOOKING_ERROR_MESSAGE)
        return redirect(url_for('book', competition=selected_competition['name'], club=selected_club['name']))

    # Check that the number of places requested is valid.
    try:
        places_required = int(request.form['places'])

        remaining_places_limit = purchase_limit(selected_club, selected_competition)

        # "Check that the required places are not equal to or less than 0."
        if places_required <= 0:
            flash(NON_POSITIVE_PLACES_MESSAGE)
            return redirect(url_for('book', competition=selected_competition['name'], club=selected_club['name']))

        # Check that the number of places requested does not exceed 12.
        if places_required > 12:
            flash(MAX_PLACES_PER_BOOKING_MESSAGE)
            return redirect(url_for('book', competition=selected_competition['name'], club=selected_club['name']))

        # "Check that the required places do not exceed the allowed places limit."
        if places_required > remaining_places_limit:
            flash(f"You can only book {remaining_places_limit} more place(s) for this competition.")
            return redirect(url_for('book', competition=selected_competition['name'], club=selected_club['name']))

        points_to_use = places_required
    except ValueError:
        flash(INVALID_PLACES_MESSAGE)
        return redirect(url_for('book', competition=selected_competition['name'], club=selected_club['name']))

    # Check if the club has enough points.
    try:
        available_points = int(selected_club['points'])
        if available_points < places_required:
            flash(INSUFFICIENT_POINTS_MESSAGE)
            return redirect(url_for('book', competition=selected_competition['name'], club=selected_club['name']))
    except ValueError:
        flash(INVALID_POINTS_MESSAGE)
        return redirect(url_for('book', competition=selected_competition['name'], club=selected_club['name']))

    # Check if there are enough places available in the competition.
    try:
        number_of_places = int(selected_competition['numberOfPlaces'])
    except ValueError:
        flash('Invalid number of places')
        return redirect(url_for('book', competition=selected_competition['name'], club=selected_club['name']))
    # Check if the competition is already full
    if number_of_places <= 0:
        flash(COMPETITION_FULL_MESSAGE)
        return redirect(url_for('book', competition=selected_competition['name'], club=selected_club['name']))

    if number_of_places < points_to_use:
        flash(INSUFFICIENT_PLACES_MESSAGE)
        return redirect(url_for('book', competition=selected_competition['name'], club=selected_club['name']))

    # If the checks are correct, we update the points and places.
    club_name = selected_club['name']
    if club_name in selected_competition['bookings']:
        selected_competition['bookings'][club_name] += places_required
    else:
        selected_competition['bookings'][club_name] = places_required

    selected_club['points'] = str(available_points - points_to_use)
    selected_competition['numberOfPlaces'] = str(number_of_places - places_required)

    # Save changes if all checks are correct
    save_success = save_clubs(clubs) and save_competitions(competitions)
    if not save_success:
        flash(SAVE_CHANGES_MESSAGE_ERROR)
        return redirect(url_for('book', competition=selected_competition['name'], club=selected_club['name']))

    # Generate and display the confirmation message
    booking_confirmation_message = (f"You have reserved {places_required} place(s) for the competition"
                                    f" {selected_competition['name']}.")
    flash(BOOKING_COMPLETE_MESSAGE)
    flash(booking_confirmation_message)

    return render_template('welcome.html', club=selected_club, competitions=competitions)


@app.route('/club-points')
def club_points():
    clubs = load_clubs()
    if not clubs:
        flash(LOADING_MESSAGE_ERROR)
        return redirect(url_for('index'))
    return render_template('club_points.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

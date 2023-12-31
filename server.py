import json
from flask import Flask, render_template, request, redirect, flash, url_for

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


def loadClubs():
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def loadCompetitions():
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


def save_clubs(club_list):
    with open('clubs.json', 'w') as c:
        json.dump({"clubs": club_list}, c, indent=4)


def save_competitions(competition_list):
    with open('competitions.json', 'w') as comps:
        json.dump({"competitions": competition_list}, comps, indent=4)


app = Flask(__name__)
app.secret_key = 'something_special'


# competitions = loadCompetitions()
# clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form.get('email')
    clubs = loadClubs()
    competitions = loadCompetitions()

    if not email:
        flash(EMAIL_EMPTY_ERROR)
        return redirect(url_for('index'))

    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
    except IndexError:
        flash(EMAIL_NOT_FOUND_ERROR)
        return redirect(url_for('index'))
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    clubs = loadClubs()
    competitions = loadCompetitions()
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    clubs = loadClubs()
    competitions = loadCompetitions()

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

    # Check that the number of places requested is valid.
    try:
        places_required = int(request.form['places'])
        if places_required <= 0:
            flash(NON_POSITIVE_PLACES_MESSAGE)
            return redirect(url_for('book', competition=selected_competition['name'], club=selected_club['name']))

        # Check that the number of places requested does not exceed 12.
        if places_required > 12:
            flash(MAX_PLACES_PER_BOOKING_MESSAGE)
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
    if number_of_places < points_to_use:
        flash(INSUFFICIENT_PLACES_MESSAGE)
        return redirect(url_for('book', competition=selected_competition['name'], club=selected_club['name']))

    # If the checks are correct, we update the points and places.
    selected_club['points'] = available_points - points_to_use
    selected_competition['numberOfPlaces'] = number_of_places - places_required

    save_clubs(clubs)
    save_competitions(competitions)

    flash(BOOKING_COMPLETE_MESSAGE)
    return render_template('welcome.html', club=selected_club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

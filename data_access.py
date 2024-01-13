import os
import json


def loadClubs():
    env = os.getenv('FLASK_ENV', 'production')
    file_path = 'data/production/clubs.json' if env == 'production' \
        else 'data/test/clubs_test.json'

    try:
        with open(file_path, 'r') as c:
            list_of_clubs = json.load(c)['clubs']
            return list_of_clubs
    except(FileNotFoundError, json.decoder.JSONDecodeError) as e:
        print(f"Error loading {file_path}: {e}")
        return []  # Return an empty list in case of error.


def loadCompetitions():
    env = os.getenv('FLASK_ENV', 'production')
    file_path = 'data/production/competitions.json' if env == 'production' \
        else 'data/test/competitions_test.json'
    try:
        with open(file_path, 'r') as c:
            list_of_competitions = json.load(c)['competitions']
            return list_of_competitions
    except(FileNotFoundError, json.decoder.JSONDecodeError) as e:
        print(f"Error loading {file_path}: {e}")
        return []  # Return an empty list in case of error.


def save_clubs(clubs_list) -> bool:
    env = os.getenv('FLASK_ENV', 'production')
    file_path = 'data/production/clubs.json' if env == 'production' \
        else 'data/test/clubs_test.json'

    try:
        with open(file_path, 'w') as c:
            json.dump({"clubs": clubs_list}, c, indent=4)
            return True  # Returns True if writing was successful
    except IOError as e:
        print(f"Error saving to {file_path}: {e}")
        return False  # Returns False if an error occurs


def save_competitions(competitions_list) -> bool:
    env = os.getenv('FLASK_ENV', 'production')
    file_path = 'data/production/competitions.json' if env == 'production' \
        else 'data/test/competitions_test.json'
    try:
        with open(file_path, 'w') as c:
            json.dump({"competitions": competitions_list}, c, indent=4)
            return True  # Returns True if writing was successful
    except IOError as e:
        print(f"Error saving to {file_path}: {e}")
        return False  # Returns False if an error occurs

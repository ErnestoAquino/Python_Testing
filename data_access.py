import json


def loadClubs(file_path='clubs.json'):
    try:
        with open(file_path, 'r') as c:
            list_of_clubs = json.load(c)['clubs']
            return list_of_clubs
    except(FileNotFoundError, json.decoder.JSONDecodeError) as e:
        print(f"Error loading {file_path}: {e}")
        return []  # Return an empty list in case of error.


def loadCompetitions(file_path='competitions.json'):
    try:
        with open(file_path, 'r') as c:
            list_of_competitions = json.load(c)['competitions']
            return list_of_competitions
    except(FileNotFoundError, json.decoder.JSONDecodeError) as e:
        print(f"Error loading {file_path}: {e}")
        return []   # Return an empty list in case of error.


def save_clubs(clubs_list, file_path='clubs.json') -> bool:
    try:
        with open(file_path, 'w') as c:
            json.dump({"clubs": clubs_list}, c, indent=4)
            return True  # Returns True if writing was successful
    except IOError as e:
        print(f"Error saving to {file_path}: {e}")
        return False  # Returns False if an error occurs


def save_competitions(competitions_list, file_path='competitions.json') -> bool:
    try:
        with open(file_path, 'w') as c:
            json.dump({"competitions": competitions_list}, c, indent=4)
            return True  # Returns True if writing was successful
    except IOError as e:
        print(f"Error saving to {file_path}: {e}")
        return False  # Returns False if an error occurs

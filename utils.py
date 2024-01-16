from datetime import datetime
from typing import Optional


def parse_competition_date(date_str: str) -> Optional[datetime]:
    # Tries to convert a date string into a datetime object.
    try:
        return datetime.strptime(date_str, r"%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


def is_competition_past(competition_date: datetime, current_date: datetime) -> bool:
    # This function checks if the competition_date has already passed compared to the current_date.
    return competition_date < current_date


def purchase_limit(selected_club, selected_competition):
    # Calculates remaining booking limit for a club in a competition, ensuring it doesn't exceed the total limit of 12.
    club_name = selected_club["name"]
    current_bookings = selected_competition.get('bookings', {}).get(club_name, 0)
    return 12 - current_bookings

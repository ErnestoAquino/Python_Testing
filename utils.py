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

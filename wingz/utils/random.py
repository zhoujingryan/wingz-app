import random
from datetime import date, datetime, time, timedelta


def random_datetime(start: datetime | date, end: datetime | date) -> datetime:
    """
    Returns a random datetime from start datetime to end datetime

    Parameters:
    start (datetime): start datetime
    end (datetime): end datetime

    Returns:
    datetime: random datetime
    """
    delta = end - start
    int_delta = int(delta.total_seconds())
    random_second = random.randint(0, int_delta)
    start_date = start if isinstance(start, date) else start.date
    start_time = time.min if isinstance(start, date) else start.time()
    return datetime.combine(start_date, start_time) + timedelta(seconds=random_second)


def random_longitude(min_lon: float = -180, max_lon: float = 180) -> float:
    """
    Returns a random longitude within the specified range

    Parameters:
    min_lon (float): Minimum longitude value
    max_lon (float): Maximum longitude value

    Returns:
    float: Random longitude within the valid range
    """
    min_lon = max(-180, min(180, min_lon))
    max_lon = max(-180, min(180, max_lon))

    if min_lon > max_lon:
        min_lon, max_lon = max_lon, min_lon

    return random.uniform(min_lon, max_lon)


def random_latitude(min_lat: float = -90, max_lat: float = 90) -> float:
    """
    Returns a random latitude within the specified range

    Parameters:
    min_lat (float): Minimum latitude value
    max_lat (float): Maximum latitude value

    Returns:
    float: Random latitude within the valid range
    """
    min_lat = max(-90, min(90, min_lat))
    max_lat = max(-90, min(90, max_lat))

    if min_lat > max_lat:
        min_lat, max_lat = max_lat, min_lat

    return random.uniform(min_lat, max_lat)

from app.repositories.event_repository import fetch_upcoming_events

MAX_LIMIT = 100
DEFAULT_LIMIT = 10

def get_upcoming_events(limit: int = DEFAULT_LIMIT) -> list[dict]:
    limit = max(1, min(limit, MAX_LIMIT))
    return fetch_upcoming_events(limit)
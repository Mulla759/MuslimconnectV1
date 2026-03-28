"""Business logic for event retrieval and validation."""
from app.repositories.event_repository import get_upcoming_events


def fetch_upcoming_events(limit: int) -> list[dict]:
    """Fetch and return upcoming events constrained by API-level limit rules."""
    safe_limit = max(1, min(limit, 100))
    return get_upcoming_events(limit=safe_limit)

"""Controller functions that shape event API responses."""
from app.models.event import EventSummary, UpcomingEventsResponse
from app.services.event_service import fetch_upcoming_events


def list_upcoming_events(limit: int) -> UpcomingEventsResponse:
    """Translate service records to API response models."""
    records = fetch_upcoming_events(limit=limit)
    items = [EventSummary.model_validate(record) for record in records]
    return UpcomingEventsResponse(items=items, count=len(items))

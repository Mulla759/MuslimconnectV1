from app.services.event_service import get_upcoming_events
from app.models.event import EventItem, EventsResponse

def upcoming_events_controller(limit: int) -> EventsResponse:
    raw = get_upcoming_events(limit)
    items = [EventItem(**row) for row in raw]
    return EventsResponse(items=items, count=len(items))

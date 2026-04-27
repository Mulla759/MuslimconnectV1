from fastapi import HTTPException

from app.models.event import EventItem, EventsResponse
from app.services.event_service import get_event_by_id, get_upcoming_events


def upcoming_events_controller(limit: int) -> EventsResponse:
    raw = get_upcoming_events(limit)
    items = [EventItem(**row) for row in raw]
    return EventsResponse(items=items, count=len(items))

def event_detail_controller(event_id: int) -> EventItem:
    raw = get_event_by_id(event_id)
    if not raw:
        raise HTTPException(status_code=404, detail="Event not found")
    return EventItem(**raw)
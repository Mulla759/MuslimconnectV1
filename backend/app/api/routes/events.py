from fastapi import APIRouter, Query

from app.controllers.events_controller import event_detail_controller, upcoming_events_controller
from app.models.event import EventItem, EventsResponse

router = APIRouter()

@router.get("/events/upcoming", response_model=EventsResponse)
def get_upcoming_events(limit: int = Query(default=10, ge=1, le=100)):
    return upcoming_events_controller(limit)

@router.get("/events/{event_id}", response_model=EventItem)
def get_event(event_id: int):
    return event_detail_controller(event_id)
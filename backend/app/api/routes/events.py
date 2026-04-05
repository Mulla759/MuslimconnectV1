from fastapi import APIRouter, Query

from app.controllers.events_controller import upcoming_events_controller
from app.models.event import EventsResponse

router = APIRouter()


@router.get("/events/upcoming", response_model=EventsResponse)
def get_upcoming_events(limit: int = Query(default=10, ge=1, le=100)) -> EventsResponse:
    return upcoming_events_controller(limit)

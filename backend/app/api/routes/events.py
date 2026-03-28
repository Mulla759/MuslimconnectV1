"""Event routes that expose upcoming event read APIs."""
from fastapi import APIRouter, Query

from app.controllers.events_controller import list_upcoming_events
from app.models.event import UpcomingEventsResponse

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/upcoming", response_model=UpcomingEventsResponse)
def get_upcoming_events(limit: int = Query(default=10, ge=1, le=100)) -> UpcomingEventsResponse:
    """Return upcoming non-cancelled events sorted by start time."""
    return list_upcoming_events(limit=limit)

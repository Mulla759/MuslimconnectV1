"""Event domain models used by API request/response payloads."""
from pydantic import BaseModel


class EventSummary(BaseModel):
    """Compact event payload consumed by dashboard-style event feeds."""

    id: int
    organization_id: int
    organization_name: str
    organization_verified: bool
    title: str
    description: str | None
    location: str
    start_datetime: str
    end_datetime: str | None
    status: str


class UpcomingEventsResponse(BaseModel):
    """Envelope for the `GET /events/upcoming` response."""

    items: list[EventSummary]
    count: int

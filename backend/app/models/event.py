from pydantic import BaseModel


class EventItem(BaseModel):
    id: int
    organization_id: int
    organization_name: str
    organization_verified: bool
    title: str
    description: str | None = None
    location: str
    start_datetime: str
    end_datetime: str | None = None
    status: str


class EventsResponse(BaseModel):
    items: list[EventItem]
    count: int

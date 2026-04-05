from pydantic import BaseModel
from typing import Optional

class EventItem(BaseModel):
    id: int
    organization_id: int
    organization_name: str
    organization_verified: bool
    title: str
    description: Optional[str] = None
    location: str
    start_datetime: str
    end_datetime: Optional[str] = None
    status: str

class EventsResponse(BaseModel):
    items: list[EventItem]
    count: int

from pydantic import BaseModel


class OrganizationItem(BaseModel):
    id: int
    name: str
    verified: bool
    category: str
    bio: str | None = None
    followers: int
    event_count: int

class OrganizationsResponse(BaseModel):
    items: list[OrganizationItem]
    count: int
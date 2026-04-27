from app.models.organization import OrganizationItem, OrganizationsResponse
from app.services.organization_service import get_all_organizations


def all_organizations_controller() -> OrganizationsResponse:
    raw = get_all_organizations()
    items = [OrganizationItem(**row) for row in raw]
    return OrganizationsResponse(items=items, count=len(items))
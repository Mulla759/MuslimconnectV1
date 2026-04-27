from fastapi import APIRouter

from app.controllers.organizations_controller import all_organizations_controller
from app.models.organization import OrganizationsResponse

router = APIRouter()

@router.get("/organizations", response_model=OrganizationsResponse)
def get_organizations():
    return all_organizations_controller()
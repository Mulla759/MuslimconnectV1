from fastapi import APIRouter

from app.controllers.auth_controller import login_controller, register_controller
from app.models.user import AuthResponse, LoginRequest, RegisterRequest

router = APIRouter()

@router.post("/auth/register", response_model=AuthResponse)
def register(data: RegisterRequest):
    return register_controller(data)

@router.post("/auth/login", response_model=AuthResponse)
def login(data: LoginRequest):
    return login_controller(data)

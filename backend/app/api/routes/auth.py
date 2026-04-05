from fastapi import APIRouter
from app.models.user import RegisterRequest, LoginRequest, AuthResponse
from app.controllers.auth_controller import register_controller, login_controller

router = APIRouter()

@router.post("/auth/register", response_model=AuthResponse)
def register(data: RegisterRequest):
    return register_controller(data)

@router.post("/auth/login", response_model=AuthResponse)
def login(data: LoginRequest):
    return login_controller(data)

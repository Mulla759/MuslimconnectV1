from fastapi import HTTPException
from app.services.auth_service import register_user, login_user
from app.models.user import RegisterRequest, LoginRequest, AuthResponse

def register_controller(data: RegisterRequest) -> AuthResponse:
    result, error = register_user(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        password=data.password,
        campus=data.campus
    )
    if error:
        raise HTTPException(status_code=400, detail=error)
    return AuthResponse(**result)

def login_controller(data: LoginRequest) -> AuthResponse:
    result, error = login_user(email=data.email, password=data.password)
    if error:
        raise HTTPException(status_code=401, detail=error)
    return AuthResponse(**result)

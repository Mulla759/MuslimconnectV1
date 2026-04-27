
from pydantic import BaseModel


class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    campus: str | None = None

class LoginRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    token: str
    user_id: int
    email: str
    first_name: str
    last_name: str
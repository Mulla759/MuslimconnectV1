from pydantic import BaseModel
from typing import Optional

class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    campus: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    token: str
    user_id: int
    email: str
    first_name: str
    last_name: str
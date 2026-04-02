import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: str = ""
    institution: str | None = None


class UserRead(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str
    full_name: str
    is_verified_scientist: bool
    institution: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

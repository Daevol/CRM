from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.models.user import UserRole


class UserBase(BaseModel):
    full_name: str
    phone: str
    role: UserRole = UserRole.CLIENT


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[UserRole] = None

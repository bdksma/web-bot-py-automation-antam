from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    full_name: str
    phone: Optional[str]
    antam_username: str
    antam_password: str
    preferred_min_gram: Optional[int] = 1
    preferred_max_gram: Optional[int] = 100


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # ✅ Pydantic v2
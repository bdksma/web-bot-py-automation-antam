from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# =====================
# BASE
# =====================
class UserBase(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None

    antam_username: str = Field(..., min_length=3, max_length=100)
    antam_password: str = Field(..., min_length=6, max_length=255)

    preferred_min_gram: int = Field(default=5, ge=1)
    preferred_max_gram: int = Field(default=50, le=100)


# =====================
# CREATE
# =====================
class UserCreate(UserBase):
    pass


# =====================
# RESPONSE
# =====================
class UserResponse(UserBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    id: str
    is_email_verified: bool = False
    two_factor_enabled: bool = False
    created_at: Optional[datetime] = None


class UserInDB(UserBase):
    id: Optional[str] = None
    hashed_password: str
    is_email_verified: bool = False
    two_factor_enabled: bool = True
    otp_code: Optional[str] = None
    otp_expires_at: Optional[datetime] = None
    failed_login_attempts: int = 0
    locked_until: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {datetime: lambda v: v.isoformat()}

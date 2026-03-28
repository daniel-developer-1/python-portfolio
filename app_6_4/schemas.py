from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=30)
    age: int = Field(..., gt=18)
    email: EmailStr
    working: bool


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=30)
    age: Optional[int] = Field(None, gt=18)
    email: Optional[EmailStr]
    working: Optional[bool]


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

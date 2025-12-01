from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "pending"


class TaskUpdate(BaseModel):
    status: str


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    user_id: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ValidatedUser(BaseModel):
    user_id: int
    role: str
    email: str

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ContactCreate(BaseModel):
    name: str
    discription: Optional[str] = ""


class ContactInfo(BaseModel):
    id: int
    name: str
    discription: str
    created_at: datetime
    updated_at: datetime

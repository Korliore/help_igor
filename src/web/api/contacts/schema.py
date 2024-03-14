from pydantic import BaseModel
from typing import Optional


class ContactCreate(BaseModel):
    name: str
    discription: Optional[str] = ""

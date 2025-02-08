from typing import Optional
from pydantic import BaseModel, Field


class User(BaseModel):
    id: Optional[int] = Field(None, description="Should be automatically asigned")
    name: str = Field(min_length=3, max_length=15)
    email: str = Field(min_length=3, max_length=300) #no optional, age range

class Company(BaseModel):
    id: int
    name: str = Field(min_length=3, max_length=15)
    userId: int = Field(None)


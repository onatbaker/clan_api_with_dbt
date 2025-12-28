from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class ClanCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    region: str = Field(pattern=r"^[A-Z]{2}$") # region abbreviations can only be 2 letters according to the alpha-2 regulations (3 for alpha-3 but example csv was with 2 lettered versions)

class ClanOut(BaseModel):
    id: UUID
    name: str
    region: str
    created_at: datetime

    class Config:
        from_attributes = True

from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.attachment import AttachmentRead

class IncidentBase(BaseModel):
    type: str = Field(max_length=50)
    description: str
    location: str = Field(max_length=255)
    status: str = "reported"
    source: str = ""
    latitude: float
    longitude: float

class IncidentCreate(IncidentBase):
    pass

class IncidentRead(IncidentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    attachments: list[AttachmentRead] = []
    model_config = {"from_attributes": True}

from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.attachment import AttachmentRead

class RoadStatusBase(BaseModel):
    road_name: str = Field(max_length=255)
    status: str = "open"
    details: str = ""
    source: str = ""
    effective_from: datetime | None = None
    effective_to: datetime | None = None

class RoadStatusCreate(RoadStatusBase):
    pass

class RoadStatusRead(RoadStatusBase):
    id: int
    updated_at: datetime
    attachments: list[AttachmentRead] = []
    model_config = {"from_attributes": True}

from datetime import datetime
from pydantic import BaseModel

class AttachmentRead(BaseModel):
    id: int
    url: str
    filename: str
    mime_type: str
    size: int
    created_at: datetime
    model_config = {"from_attributes": True}

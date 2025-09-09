from datetime import datetime
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class RoadStatus(Base):
    __tablename__ = "road_status"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    road_name: Mapped[str] = mapped_column(String(255), index=True)
    status: Mapped[str] = mapped_column(String(50), index=True, default="open")
    details: Mapped[str] = mapped_column(String(500), default="")
    source: Mapped[str] = mapped_column(String(255), default="")
    effective_from: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    effective_to: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    attachments = relationship("Attachment", back_populates="road_status", cascade="all, delete-orphan")

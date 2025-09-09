from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Text, Float, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Incident(Base):
    __tablename__ = "incidents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    type: Mapped[str] = mapped_column(String(50), index=True)
    description: Mapped[str] = mapped_column(Text)
    location: Mapped[str] = mapped_column(String(255), index=True)
    status: Mapped[str] = mapped_column(String(50), index=True, default="reported")
    source: Mapped[str] = mapped_column(String(255), default="")
    latitude: Mapped[float] = mapped_column(Float, index=True)
    longitude: Mapped[float] = mapped_column(Float, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    attachments = relationship("Attachment", back_populates="incident", cascade="all, delete-orphan")

Index("ix_incidents_lat_lng", Incident.latitude, Incident.longitude)

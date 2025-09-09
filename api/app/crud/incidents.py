from sqlalchemy.orm import Session
from sqlalchemy import select, desc, and_
from app.models.incident import Incident
from app.schemas.incident import IncidentCreate

def create_incident(db: Session, data: IncidentCreate) -> Incident:
    obj = Incident(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_incidents(db: Session, limit: int = 100, incident_type: str | None = None, bbox: tuple[float, float, float, float] | None = None) -> list[Incident]:
    stmt = select(Incident).order_by(desc(Incident.created_at)).limit(limit)
    if incident_type:
        stmt = stmt.where(Incident.type == incident_type)
    if bbox:
        west, south, east, north = bbox
        stmt = stmt.where(
            and_(
                Incident.longitude >= west,
                Incident.longitude <= east,
                Incident.latitude >= south,
                Incident.latitude <= north,
            )
        )
    return list(db.execute(stmt).scalars().all())

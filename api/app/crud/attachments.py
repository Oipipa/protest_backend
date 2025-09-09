from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.attachment import Attachment
from app.models.incident import Incident
from app.models.road_status import RoadStatus

def ensure_incident(db: Session, incident_id: int) -> Incident:
    obj = db.get(Incident, incident_id)
    if not obj:
        raise ValueError("incident_not_found")
    return obj

def ensure_road(db: Session, road_id: int) -> RoadStatus:
    obj = db.get(RoadStatus, road_id)
    if not obj:
        raise ValueError("road_not_found")
    return obj

def add_incident_attachments(db: Session, incident_id: int, items: list[dict]) -> list[Attachment]:
    ensure_incident(db, incident_id)
    rows = []
    for it in items:
        a = Attachment(incident_id=incident_id, filename=it["filename"], mime_type=it["mime_type"], size=it["size"], url=it["url"])
        db.add(a)
        rows.append(a)
    db.commit()
    for a in rows:
        db.refresh(a)
    return rows

def add_road_attachments(db: Session, road_id: int, items: list[dict]) -> list[Attachment]:
    ensure_road(db, road_id)
    rows = []
    for it in items:
        a = Attachment(road_status_id=road_id, filename=it["filename"], mime_type=it["mime_type"], size=it["size"], url=it["url"])
        db.add(a)
        rows.append(a)
    db.commit()
    for a in rows:
        db.refresh(a)
    return rows

def list_incident_attachments(db: Session, incident_id: int) -> list[Attachment]:
    return list(db.execute(select(Attachment).where(Attachment.incident_id == incident_id)).scalars().all())

def list_road_attachments(db: Session, road_id: int) -> list[Attachment]:
    return list(db.execute(select(Attachment).where(Attachment.road_status_id == road_id)).scalars().all())

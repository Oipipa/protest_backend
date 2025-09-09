from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from app.models.road_status import RoadStatus
from app.schemas.road_status import RoadStatusCreate

def create_road_status(db: Session, data: RoadStatusCreate) -> RoadStatus:
    obj = RoadStatus(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_road_status(db: Session, limit: int = 200, road: str | None = None) -> list[RoadStatus]:
    stmt = select(RoadStatus).order_by(desc(RoadStatus.updated_at)).limit(limit)
    if road:
        stmt = stmt.where(RoadStatus.road_name == road)
    return list(db.execute(stmt).scalars().all())

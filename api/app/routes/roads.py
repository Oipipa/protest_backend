from fastapi import APIRouter, Depends, Query, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.road_status import RoadStatusCreate, RoadStatusRead
from app.schemas.attachment import AttachmentRead
from app.crud.road_status import create_road_status, list_road_status
from app.crud.attachments import add_road_attachments, list_road_attachments
from app.services.realtime import broker
from app.services.storage import save_uploads

router = APIRouter()

@router.get("/", response_model=list[RoadStatusRead])
def get_roads(limit: int = Query(200, le=1000), road: str | None = None, db: Session = Depends(get_db)):
    return list_road_status(db, limit=limit, road=road)

@router.post("/", response_model=RoadStatusRead, status_code=201)
def post_road_status(payload: RoadStatusCreate, db: Session = Depends(get_db)):
    obj = create_road_status(db, payload)
    broker.publish({"channel": "roads", "event": "updated", "data": {"id": obj.id, "road": obj.road_name}})
    return obj

@router.post("/{road_id}/attachments", response_model=list[AttachmentRead], status_code=201)
async def upload_road_attachments(road_id: int, files: list[UploadFile] = File(...), db: Session = Depends(get_db)):
    saved = await save_uploads(files, subdir=f"roads/{road_id}")
    if not saved:
        raise HTTPException(status_code=400, detail="no_valid_images")
    try:
        rows = add_road_attachments(db, road_id, saved)
    except ValueError:
        raise HTTPException(status_code=404, detail="road_not_found")
    return rows

@router.get("/{road_id}/attachments", response_model=list[AttachmentRead])
def list_road_files(road_id: int, db: Session = Depends(get_db)):
    return list_road_attachments(db, road_id)

from fastapi import APIRouter, Depends, Query, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.incident import IncidentCreate, IncidentRead
from app.schemas.attachment import AttachmentRead
from app.crud.incidents import create_incident, list_incidents
from app.crud.attachments import add_incident_attachments, list_incident_attachments
from app.services.realtime import broker
from app.services.storage import save_uploads

router = APIRouter()

def parse_bbox(bbox: str):
    parts = bbox.split(",")
    if len(parts) != 4:
        raise HTTPException(status_code=422, detail="bbox must be west,south,east,north")
    west, south, east, north = map(float, parts)
    return west, south, east, north

@router.get("/", response_model=list[IncidentRead])
def get_incidents(limit: int = Query(100, le=500), type: str | None = None, bbox: str | None = None, db: Session = Depends(get_db)):
    box = parse_bbox(bbox) if bbox else None
    return list_incidents(db, limit=limit, incident_type=type, bbox=box)

@router.get("/geojson")
def get_incidents_geojson(limit: int = Query(500, le=1000), type: str | None = None, bbox: str | None = None, db: Session = Depends(get_db)):
    box = parse_bbox(bbox) if bbox else None
    items = list_incidents(db, limit=limit, incident_type=type, bbox=box)
    features = [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [i.longitude, i.latitude]},
            "properties": {
                "id": i.id,
                "type": i.type,
                "status": i.status,
                "location": i.location,
                "source": i.source,
                "created_at": i.created_at.isoformat() + "Z",
                "updated_at": i.updated_at.isoformat() + "Z",
                "description": i.description,
            },
        }
        for i in items
    ]
    return {"type": "FeatureCollection", "features": features}

@router.post("/", response_model=IncidentRead, status_code=201)
def post_incident(payload: IncidentCreate, db: Session = Depends(get_db)):
    obj = create_incident(db, payload)
    broker.publish({"channel": "incidents", "event": "created", "data": {"id": obj.id, "type": obj.type, "lat": obj.latitude, "lng": obj.longitude}})
    return obj

@router.post("/{incident_id}/attachments", response_model=list[AttachmentRead], status_code=201)
async def upload_incident_attachments(incident_id: int, files: list[UploadFile] = File(...), db: Session = Depends(get_db)):
    saved = await save_uploads(files, subdir=f"incidents/{incident_id}")
    if not saved:
        raise HTTPException(status_code=400, detail="no_valid_images")
    try:
        rows = add_incident_attachments(db, incident_id, saved)
    except ValueError:
        raise HTTPException(status_code=404, detail="incident_not_found")
    return rows

@router.get("/{incident_id}/attachments", response_model=list[AttachmentRead])
def list_incident_files(incident_id: int, db: Session = Depends(get_db)):
    return list_incident_attachments(db, incident_id)

from fastapi import APIRouter
from app.ws.events import router as ws_router

router = APIRouter()
router.include_router(ws_router)

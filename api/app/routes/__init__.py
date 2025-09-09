from fastapi import APIRouter
from app.routes.health import router as health_router
from app.routes.incidents import router as incidents_router
from app.routes.roads import router as roads_router

router = APIRouter()
router.include_router(health_router, tags=["health"])
router.include_router(incidents_router, prefix="/incidents", tags=["incidents"])
router.include_router(roads_router, prefix="/roads", tags=["roads"])

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager, suppress
import asyncio, os
from app.core.config import settings
from app.services.logging import setup_logging  # noqa: F401
from app.db.session import engine
from app.db.base import Base
import app.models  # noqa: F401
from app.routes import router as api_router
from app.ws import router as ws_router
from app.services.realtime import broker, manager

# ensure uploads dir exists before mounting
os.makedirs(settings.upload_dir, exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    sub = asyncio.create_task(broker.run_subscriber(manager.broadcast))
    try:
        yield
    finally:
        sub.cancel()
        with suppress(BaseException):
            await sub

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=settings.upload_dir, check_dir=False), name="uploads")
app.include_router(api_router)
app.include_router(ws_router)

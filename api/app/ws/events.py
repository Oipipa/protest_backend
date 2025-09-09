from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.realtime import manager

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            msg = await ws.receive_text()
            await manager.broadcast({"channel": "client", "message": msg})
    except WebSocketDisconnect:
        await manager.disconnect(ws)

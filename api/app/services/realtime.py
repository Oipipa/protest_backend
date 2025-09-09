import asyncio
import json
import threading
from typing import Any
from redis.asyncio import Redis as AsyncRedis
from redis import Redis as SyncRedis
from fastapi import WebSocket
from app.core.config import settings
from loguru import logger

class ConnectionManager:
    def __init__(self):
        self.active: set[WebSocket] = set()
        self.lock = asyncio.Lock()

    async def connect(self, ws: WebSocket):
        await ws.accept()
        async with self.lock:
            self.active.add(ws)

    async def disconnect(self, ws: WebSocket):
        async with self.lock:
            if ws in self.active:
                self.active.remove(ws)

    async def broadcast(self, message: Any):
        data = json.dumps(message)
        async with self.lock:
            targets = list(self.active)
        for ws in targets:
            try:
                await ws.send_text(data)
            except Exception:
                await self.disconnect(ws)

class RedisBroker:
    def __init__(self, url: str, channel: str = "events"):
        self.url = url
        self.channel = channel
        self.async_client = AsyncRedis.from_url(url, decode_responses=True)
        self.sync_client = SyncRedis.from_url(url, decode_responses=True)

    def publish(self, payload: Any):
        data = payload if isinstance(payload, str) else json.dumps(payload)
        try:
            loop = asyncio.get_running_loop()
            asyncio.create_task(self.async_client.publish(self.channel, data))
        except RuntimeError:
            threading.Thread(target=self.sync_client.publish, args=(self.channel, data), daemon=True).start()

    async def run_subscriber(self, callback):
        async with self.async_client.pubsub() as pubsub:
            await pubsub.subscribe(self.channel)
            try:
                async for m in pubsub.listen():
                    if m and m.get("type") == "message":
                        try:
                            await callback(json.loads(m["data"]))
                        except Exception as e:
                            logger.error(f"subscriber_error {e}")
            except asyncio.CancelledError:
                return

manager = ConnectionManager()
broker = RedisBroker(settings.redis_url)

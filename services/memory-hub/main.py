from __future__ import annotations

import os
import json
from typing import Any, Dict, List

import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

app = FastAPI(title="memory-hub")
client = redis.Redis.from_url(REDIS_URL, decode_responses=True)


class MemoryItem(BaseModel):
    key: str
    value: Dict[str, Any]


@app.get("/memory/{session_id}")
async def get_session(session_id: str):
    data = client.get(session_id)
    if not data:
        return {"session_id": session_id, "items": []}
    return {"session_id": session_id, "items": json.loads(data)}


@app.post("/memory/{session_id}")
async def set_session(session_id: str, items: List[MemoryItem]):
    payload = [i.model_dump() for i in items]
    client.set(session_id, json.dumps(payload))
    return {"ok": True}


@app.post("/memory/{session_id}/append")
async def append_item(session_id: str, item: MemoryItem):
    data = client.get(session_id)
    items = json.loads(data) if data else []
    items.append(item.model_dump())
    client.set(session_id, json.dumps(items))
    return {"ok": True, "size": len(items)}


@app.get("/health")
async def health():
    return {"ok": True}

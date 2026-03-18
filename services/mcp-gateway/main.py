from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from api2mcp_engine import invoke_tool_from_config
from registry import ToolRegistry
from streaming import stream_agent

TOOL_HUB_URL = os.getenv("TOOL_HUB_URL")
TOOL_CONFIG_DIR = os.getenv("TOOL_CONFIG_DIR", str(Path(__file__).resolve().parents[2] / "examples"))

app = FastAPI(title="mcp-gateway")
registry = ToolRegistry(TOOL_CONFIG_DIR)


@app.get("/tools")
async def list_tools():
    if TOOL_HUB_URL:
        async with httpx.AsyncClient() as client:
            resp = await client.get(TOOL_HUB_URL.rstrip("/") + "/tools")
        return resp.json()
    registry.load()
    return {"tools": [t.model_dump() for t in registry.list_tools()]}


@app.post("/invoke")
async def invoke(payload: Dict[str, Any]):
    tool_name = payload.get("tool_name")
    inputs = payload.get("inputs", {})
    version = payload.get("version")
    if not tool_name:
        raise HTTPException(status_code=400, detail="tool_name required")
    if TOOL_HUB_URL:
        async with httpx.AsyncClient() as client:
            tool_resp = await client.get(TOOL_HUB_URL.rstrip("/") + f"/tools/{tool_name}", params={"version": version} if version else None)
        if tool_resp.status_code >= 400:
            raise HTTPException(status_code=tool_resp.status_code, detail=tool_resp.text)
        config = tool_resp.json()
    else:
        registry.load()
        config = registry.load_config(tool_name, version)
        if not config:
            raise HTTPException(status_code=404, detail="tool not found")

    result = await invoke_tool_from_config(config, inputs)
    return result


@app.post("/stream")
async def stream(payload: Dict[str, Any]):
    return StreamingResponse(stream_agent(payload), media_type="text/event-stream")


@app.get("/health")
async def health():
    return {"ok": True}

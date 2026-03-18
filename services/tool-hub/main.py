from __future__ import annotations

import os
from pathlib import Path
from fastapi import FastAPI, HTTPException

from registry import ToolRegistry

ROOT_DIR = os.getenv("TOOL_CONFIG_DIR", str(Path(__file__).resolve().parents[2] / "examples"))

app = FastAPI(title="tool-hub")
registry = ToolRegistry(ROOT_DIR)
registry.load()


@app.get("/tools")
async def list_tools():
    registry.load()
    return {"tools": [t.model_dump() for t in registry.list_tools()]}


@app.get("/tools/{name}")
async def get_tool(name: str, version: str | None = None):
    registry.load()
    config = registry.load_config(name, version)
    if not config:
        raise HTTPException(status_code=404, detail="tool not found")
    return config


@app.get("/health")
async def health():
    return {"ok": True}

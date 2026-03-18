from __future__ import annotations

from fastapi import FastAPI

from models import InvokeRequest, InvokeResult
from engine import invoke_tool

app = FastAPI(title="api2mcp-engine")


@app.post("/invoke", response_model=InvokeResult)
async def invoke(req: InvokeRequest) -> InvokeResult:
    return await invoke_tool(req.config, req.inputs)


@app.get("/health")
async def health() -> dict:
    return {"ok": True}

from __future__ import annotations

import asyncio
import json
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from runtime import AgentRunRequest, run_agent

app = FastAPI(title="agent-runtime")


@app.post("/run")
async def run(req: AgentRunRequest):
    return await run_agent(req)


async def _stream(req: AgentRunRequest) -> AsyncGenerator[bytes, None]:
    result = await run_agent(req)
    # Stream tokens
    for token in result.final.split(" "):
        yield f"event: token\ndata: {token}\n\n".encode("utf-8")
        await asyncio.sleep(0.02)
    # Stream steps
    for step in result.steps:
        yield f"event: tool_call\ndata: {step.model_dump_json()}\n\n".encode("utf-8")
        await asyncio.sleep(0.01)
    yield f"event: result\ndata: {result.model_dump_json()}\n\n".encode("utf-8")


@app.post("/stream")
async def stream(req: AgentRunRequest):
    return StreamingResponse(_stream(req), media_type="text/event-stream")


@app.get("/health")
async def health():
    return {"ok": True}

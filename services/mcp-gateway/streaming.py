from __future__ import annotations

import asyncio
import json
from typing import Any, AsyncGenerator, Dict

import httpx


async def stream_agent(payload: Dict[str, Any]) -> AsyncGenerator[bytes, None]:
    # Agent protocol: payload includes message, optional tool_endpoint
    message = payload.get("message", "")
    tool_endpoint = payload.get("tool_endpoint", "http://localhost:8000")

    # Emit a token stream of the message
    for token in message.split(" "):
        yield f"event: token\ndata: {token}\n\n".encode("utf-8")
        await asyncio.sleep(0.02)

    # If a tool is requested with protocol: tool:<name> {json}
    if "tool:" in message:
        try:
            _, rest = message.split("tool:", 1)
            rest = rest.strip()
            name, payload_json = rest.split(" ", 1)
            args = json.loads(payload_json)
            yield f"event: tool_call\ndata: {{\"name\": \"{name}\", \"arguments\": {json.dumps(args)} }}\n\n".encode("utf-8")
            async with httpx.AsyncClient(trust_env=False) as client:
                resp = await client.post(tool_endpoint.rstrip("/") + "/invoke", json={"tool_name": name, "inputs": args})
            yield f"event: result\ndata: {resp.text}\n\n".encode("utf-8")
        except Exception as exc:
            yield f"event: result\ndata: {{\"ok\": false, \"error\": \"{str(exc)}\"}}\n\n".encode("utf-8")
    else:
        yield f"event: result\ndata: {{\"ok\": true, \"message\": \"No tool call in message\"}}\n\n".encode("utf-8")

from __future__ import annotations

import asyncio
import json
import time
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ToolCall(BaseModel):
    name: str
    arguments: Dict[str, Any]


class AgentStep(BaseModel):
    thought: str
    tool_call: Optional[ToolCall] = None
    observation: Optional[Any] = None


class AgentRunRequest(BaseModel):
    message: str
    tools: List[Dict[str, Any]]
    tool_endpoint: str


class AgentRunResult(BaseModel):
    ok: bool
    final: str
    steps: List[AgentStep]
    latency_ms: int


def _extract_tool_call(message: str) -> Optional[ToolCall]:
    # Simple protocol: "tool:<name> {json}" anywhere in the message
    if "tool:" not in message:
        return None
    try:
        prefix, rest = message.split("tool:", 1)
        rest = rest.strip()
        name, payload = rest.split(" ", 1)
        args = json.loads(payload)
        return ToolCall(name=name.strip(), arguments=args)
    except Exception:
        return None


async def run_agent(req: AgentRunRequest) -> AgentRunResult:
    start = time.time()
    steps: List[AgentStep] = []
    tool_call = _extract_tool_call(req.message)
    final = ""

    if tool_call is None:
        final = "No tool call requested. Use 'tool:<name> {json}' to call a tool."
    else:
        steps.append(AgentStep(thought=f"Calling tool {tool_call.name}", tool_call=tool_call))
        import httpx
        async with httpx.AsyncClient(trust_env=False) as client:
            resp = await client.post(
                req.tool_endpoint.rstrip("/") + "/invoke",
                json={"tool_name": tool_call.name, "inputs": tool_call.arguments},
            )
        if resp.status_code >= 400:
            steps.append(AgentStep(thought="Tool error", observation=resp.text))
            final = f"Tool call failed: {resp.text}"
        else:
            payload = resp.json()
            steps.append(AgentStep(thought="Tool result", observation=payload))
            final = f"Tool result: {json.dumps(payload)}"

    latency_ms = int((time.time() - start) * 1000)
    return AgentRunResult(ok=True, final=final, steps=steps, latency_ms=latency_ms)

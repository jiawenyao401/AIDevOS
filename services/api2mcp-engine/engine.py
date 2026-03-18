from __future__ import annotations

import asyncio
import re
import time
from typing import Any, Dict

import httpx
from jsonpath_ng import parse as jsonpath_parse

from models import ToolConfig, InvokeResult

_TEMPLATE_RE = re.compile(r"\{\{\s*input\.([\w\.-]+)\s*\}\}")


def _get_by_path(data: Dict[str, Any], path: str) -> Any:
    cur: Any = data
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur


def _resolve_templates(obj: Any, inputs: Dict[str, Any]) -> Any:
    if isinstance(obj, str):
        def _replace(match: re.Match[str]) -> str:
            val = _get_by_path(inputs, match.group(1))
            return "" if val is None else str(val)
        return _TEMPLATE_RE.sub(_replace, obj)
    if isinstance(obj, list):
        return [_resolve_templates(x, inputs) for x in obj]
    if isinstance(obj, dict):
        return {k: _resolve_templates(v, inputs) for k, v in obj.items()}
    return obj


def _apply_auth(headers: Dict[str, Any], query: Dict[str, Any], auth: Any) -> None:
    if auth.type == "api_key":
        if auth.header:
            headers[auth.header] = auth.value or ""
        if auth.query_param:
            query[auth.query_param] = auth.value or ""
    elif auth.type == "bearer":
        headers["Authorization"] = f"Bearer {auth.value or ''}"


def _map_output(output_mapping: Dict[str, Any], response_json: Any) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for key, expr in output_mapping.items():
        try:
            jsonpath = jsonpath_parse(expr)
            matches = [m.value for m in jsonpath.find(response_json)]
            if len(matches) == 1:
                result[key] = matches[0]
            else:
                result[key] = matches
        except Exception:
            result[key] = None
    return result


async def invoke_tool(config: ToolConfig, inputs: Dict[str, Any]) -> InvokeResult:
    headers = _resolve_templates(dict(config.request.headers), inputs)
    query = _resolve_templates(dict(config.request.query), inputs)
    body = _resolve_templates(dict(config.request.body), inputs)

    _apply_auth(headers, query, config.auth)

    attempt = 0
    start = time.time()
    last_error = None
    while attempt <= config.request.retries:
        attempt += 1
        try:
            async with httpx.AsyncClient(timeout=config.request.timeout_ms / 1000, trust_env=False) as client:
                resp = await client.request(
                    method=config.request.method,
                    url=config.request.url,
                    headers=headers,
                    params=query,
                    json=body if body else None,
                )
            latency_ms = int((time.time() - start) * 1000)
            if resp.status_code >= 400:
                last_error = f"HTTP {resp.status_code}: {resp.text}"
                if attempt <= config.request.retries:
                    await asyncio.sleep(0.2 * attempt)
                    continue
                return InvokeResult(ok=False, error=last_error, status_code=resp.status_code, latency_ms=latency_ms, raw=resp.text)

            data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else resp.text
            mapped = _map_output(config.output_mapping, data)
            return InvokeResult(ok=True, data=mapped, status_code=resp.status_code, latency_ms=latency_ms, raw=data)
        except Exception as exc:
            last_error = str(exc)
            if attempt <= config.request.retries:
                await asyncio.sleep(0.2 * attempt)
                continue
            return InvokeResult(ok=False, error=last_error)

    return InvokeResult(ok=False, error=last_error or "unknown error")

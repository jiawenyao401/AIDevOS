from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AuthConfig(BaseModel):
    type: str = Field(..., description="api_key|bearer|none")
    header: Optional[str] = None
    query_param: Optional[str] = None
    value: Optional[str] = None


class RequestConfig(BaseModel):
    method: str
    url: str
    headers: Dict[str, Any] = {}
    query: Dict[str, Any] = {}
    body: Dict[str, Any] = {}
    timeout_ms: int = 15000
    retries: int = 1


class ToolConfig(BaseModel):
    name: str
    version: str = "0.1.0"
    description: str = ""
    auth: AuthConfig = AuthConfig(type="none")
    request: RequestConfig
    input_schema: Dict[str, Any]
    output_mapping: Dict[str, Any]


class InvokeRequest(BaseModel):
    config: ToolConfig
    inputs: Dict[str, Any]


class InvokeResult(BaseModel):
    ok: bool
    data: Dict[str, Any] = {}
    error: Optional[str] = None
    status_code: Optional[int] = None
    latency_ms: Optional[int] = None
    raw: Optional[Any] = None

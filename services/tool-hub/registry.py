from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel


class ToolIndex(BaseModel):
    name: str
    version: str
    description: str = ""
    config_path: str


class ToolRegistry:
    def __init__(self, root_dir: str) -> None:
        self.root_dir = Path(root_dir)
        self._index: Dict[str, List[ToolIndex]] = {}

    def load(self) -> None:
        self._index.clear()
        for path in self.root_dir.rglob("*.json"):
            try:
                raw = json.loads(path.read_text(encoding="utf-8-sig"))
                name = raw.get("name")
                version = raw.get("version", "0.1.0")
                desc = raw.get("description", "")
                if not name:
                    continue
                entry = ToolIndex(name=name, version=version, description=desc, config_path=str(path))
                self._index.setdefault(name, []).append(entry)
            except Exception:
                continue
        for name in list(self._index.keys()):
            self._index[name].sort(key=lambda x: x.version, reverse=True)

    def list_tools(self) -> List[ToolIndex]:
        return [v[0] for v in self._index.values()]

    def get_tool(self, name: str, version: Optional[str] = None) -> Optional[ToolIndex]:
        if name not in self._index:
            return None
        if version is None:
            return self._index[name][0]
        for entry in self._index[name]:
            if entry.version == version:
                return entry
        return None

    def load_config(self, name: str, version: Optional[str] = None) -> Optional[dict]:
        entry = self.get_tool(name, version)
        if not entry:
            return None
        return json.loads(Path(entry.config_path).read_text(encoding="utf-8-sig"))

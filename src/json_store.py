from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class JsonStore:
    def __init__(self, file_path: str) -> None:
        self.path = Path(file_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []

        text = self.path.read_text(encoding="utf-8").strip()
        if not text:
            return []

        data = json.loads(text)
        if not isinstance(data, list):
            raise ValueError("El archivo JSON debe contener un arreglo de objetos.")

        return [obj for obj in data if isinstance(obj, dict)]

    def save(self, records: list[dict[str, Any]]) -> None:
        tmp_path = self.path.with_suffix(".tmp")
        backup_path = self.path.with_suffix(".bak")

        tmp_path.write_text(
            json.dumps(records, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        if self.path.exists():
            self.path.replace(backup_path)

        tmp_path.replace(self.path)

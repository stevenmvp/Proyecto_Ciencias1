from __future__ import annotations

from typing import Any

from .avl_tree import AVLTree
from .json_store import JsonStore


class DatabaseManager:
    def __init__(self, file_path: str) -> None:
        self.store = JsonStore(file_path)
        self.tree = AVLTree()
        self._load_existing_data()

    def _load_existing_data(self) -> None:
        for obj in self.store.load():
            key = str(obj.get("id", "")).strip()
            if key:
                self.tree.insert(key, obj)

    def _persist(self) -> None:
        records = [obj for _, obj in self.tree.inorder_items()]
        self.store.save(records)

    def save_object(self, obj: dict[str, Any]) -> bool:
        key = str(obj.get("id", "")).strip()
        if not key:
            raise ValueError("El objeto debe incluir un id válido.")

        obj["id"] = key
        inserted = self.tree.insert(key, obj)
        if inserted:
            self._persist()
        return inserted

    def find_by_key(self, key: str) -> dict[str, Any] | None:
        return self.tree.search(str(key).strip())

    def update_object(self, key: str, new_obj: dict[str, Any]) -> bool:
        normalized_key = str(key).strip()
        if not normalized_key:
            raise ValueError("La clave no puede estar vacía.")

        new_obj["id"] = normalized_key
        updated = self.tree.update(normalized_key, new_obj)
        if updated:
            self._persist()
        return updated

    def delete_object(self, key: str) -> bool:
        deleted = self.tree.delete(str(key).strip())
        if deleted:
            self._persist()
        return deleted

    def query_by_criteria(self, field: str, value: str, mode: str = "contains") -> list[dict[str, Any]]:
        field = field.strip()
        if not field:
            return []

        records = [obj for _, obj in self.tree.inorder_items()]
        value = value.strip().lower()

        if mode == "equals":
            return [
                obj
                for obj in records
                if str(obj.get(field, "")).strip().lower() == value
            ]

        return [
            obj
            for obj in records
            if value in str(obj.get(field, "")).strip().lower()
        ]

    def all_records(self) -> list[dict[str, Any]]:
        return [obj for _, obj in self.tree.inorder_items()]

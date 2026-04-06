from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class AVLNode:
    key: str
    value: dict[str, Any]
    height: int = 1
    left: Optional["AVLNode"] = None
    right: Optional["AVLNode"] = None


class AVLTree:
    def __init__(self) -> None:
        self.root: Optional[AVLNode] = None
        self._size = 0

    @property
    def size(self) -> int:
        return self._size

    def _height(self, node: Optional[AVLNode]) -> int:
        return node.height if node else 0

    def _balance(self, node: Optional[AVLNode]) -> int:
        if not node:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _update_height(self, node: AVLNode) -> None:
        node.height = max(self._height(node.left), self._height(node.right)) + 1

    def _rotate_right(self, y: AVLNode) -> AVLNode:
        x = y.left
        t2 = x.right if x else None

        x.right = y
        y.left = t2

        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x: AVLNode) -> AVLNode:
        y = x.right
        t2 = y.left if y else None

        y.left = x
        x.right = t2

        self._update_height(x)
        self._update_height(y)
        return y

    def _rebalance(self, node: AVLNode) -> AVLNode:
        self._update_height(node)
        balance = self._balance(node)

        if balance > 1:
            if self._balance(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if balance < -1:
            if self._balance(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def insert(self, key: str, value: dict[str, Any]) -> bool:
        inserted = False

        def _insert(node: Optional[AVLNode], k: str, v: dict[str, Any]) -> AVLNode:
            nonlocal inserted
            if node is None:
                inserted = True
                return AVLNode(k, v)

            if k < node.key:
                node.left = _insert(node.left, k, v)
            elif k > node.key:
                node.right = _insert(node.right, k, v)
            else:
                return node

            return self._rebalance(node)

        self.root = _insert(self.root, key, value)
        if inserted:
            self._size += 1
        return inserted

    def search(self, key: str) -> Optional[dict[str, Any]]:
        node = self.root
        while node:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return node.value
        return None

    def update(self, key: str, value: dict[str, Any]) -> bool:
        node = self.root
        while node:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                node.value = value
                return True
        return False

    def delete(self, key: str) -> bool:
        deleted = False

        def _min_value_node(node: AVLNode) -> AVLNode:
            current = node
            while current.left:
                current = current.left
            return current

        def _delete(node: Optional[AVLNode], k: str) -> Optional[AVLNode]:
            nonlocal deleted
            if node is None:
                return None

            if k < node.key:
                node.left = _delete(node.left, k)
            elif k > node.key:
                node.right = _delete(node.right, k)
            else:
                deleted = True
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left

                successor = _min_value_node(node.right)
                node.key = successor.key
                node.value = successor.value
                node.right = _delete(node.right, successor.key)

            return self._rebalance(node) if node else None

        self.root = _delete(self.root, key)
        if deleted:
            self._size -= 1
        return deleted

    def inorder_items(self) -> list[tuple[str, dict[str, Any]]]:
        items: list[tuple[str, dict[str, Any]]] = []

        def _traverse(node: Optional[AVLNode]) -> None:
            if not node:
                return
            _traverse(node.left)
            items.append((node.key, node.value))
            _traverse(node.right)

        _traverse(self.root)
        return items

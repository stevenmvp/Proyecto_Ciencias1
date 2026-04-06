from __future__ import annotations

import tkinter as tk

from src.db_manager import DatabaseManager
from src.ui import DatabaseApp


if __name__ == "__main__":
    manager = DatabaseManager("data/database.json")
    root = tk.Tk()
    app = DatabaseApp(root, manager)
    root.mainloop()

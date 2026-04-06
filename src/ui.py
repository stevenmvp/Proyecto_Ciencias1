from __future__ import annotations

import json
import tkinter as tk
from tkinter import messagebox, ttk

from .db_manager import DatabaseManager


class DatabaseApp:
    def __init__(self, root: tk.Tk, manager: DatabaseManager) -> None:
        self.root = root
        self.manager = manager
        self.root.title("Gestor No Relacional - AVL + JSON")
        self.root.geometry("980x640")

        self.id_var = tk.StringVar()
        self.query_field_var = tk.StringVar(value="nombre")
        self.query_value_var = tk.StringVar()
        self.query_mode_var = tk.StringVar(value="contains")

        self._build_layout()
        self.refresh_table()

    def _build_layout(self) -> None:
        form_frame = ttk.LabelFrame(self.root, text="Formulario JSON")
        form_frame.pack(fill="x", padx=10, pady=8)

        ttk.Label(form_frame, text="ID:").grid(row=0, column=0, padx=6, pady=6, sticky="w")
        ttk.Entry(form_frame, textvariable=self.id_var, width=24).grid(
            row=0, column=1, padx=6, pady=6, sticky="w"
        )

        ttk.Label(form_frame, text="Objeto JSON:").grid(
            row=1, column=0, padx=6, pady=6, sticky="nw"
        )
        self.json_text = tk.Text(form_frame, height=8, width=90)
        self.json_text.grid(row=1, column=1, columnspan=5, padx=6, pady=6, sticky="we")

        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=2, column=1, columnspan=5, sticky="w", padx=6, pady=8)

        ttk.Button(btn_frame, text="Guardar", command=self.on_save).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Buscar por ID", command=self.on_find).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Actualizar", command=self.on_update).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Eliminar", command=self.on_delete).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Limpiar", command=self.on_clear).pack(side="left", padx=4)

        query_frame = ttk.LabelFrame(self.root, text="Consulta por criterios")
        query_frame.pack(fill="x", padx=10, pady=8)

        ttk.Label(query_frame, text="Campo:").grid(row=0, column=0, padx=6, pady=6)
        ttk.Entry(query_frame, textvariable=self.query_field_var, width=20).grid(
            row=0, column=1, padx=6, pady=6
        )

        ttk.Label(query_frame, text="Valor:").grid(row=0, column=2, padx=6, pady=6)
        ttk.Entry(query_frame, textvariable=self.query_value_var, width=25).grid(
            row=0, column=3, padx=6, pady=6
        )

        ttk.Radiobutton(
            query_frame,
            text="Contiene",
            variable=self.query_mode_var,
            value="contains",
        ).grid(row=0, column=4, padx=6, pady=6)

        ttk.Radiobutton(
            query_frame,
            text="Igual a",
            variable=self.query_mode_var,
            value="equals",
        ).grid(row=0, column=5, padx=6, pady=6)

        ttk.Button(query_frame, text="Consultar", command=self.on_query).grid(
            row=0, column=6, padx=8, pady=6
        )
        ttk.Button(query_frame, text="Ver todos", command=self.refresh_table).grid(
            row=0, column=7, padx=8, pady=6
        )

        table_frame = ttk.LabelFrame(self.root, text="Registros")
        table_frame.pack(fill="both", expand=True, padx=10, pady=8)

        self.table = ttk.Treeview(table_frame, columns=("id", "data"), show="headings")
        self.table.heading("id", text="ID")
        self.table.heading("data", text="Objeto JSON")
        self.table.column("id", width=130, anchor="w")
        self.table.column("data", width=780, anchor="w")
        self.table.pack(fill="both", expand=True, padx=6, pady=6)

        self.table.bind("<<TreeviewSelect>>", self.on_select_row)

    def _read_json_payload(self) -> dict:
        payload = self.json_text.get("1.0", tk.END).strip()
        if not payload:
            raise ValueError("Debes escribir un objeto JSON.")

        obj = json.loads(payload)
        if not isinstance(obj, dict):
            raise ValueError("El contenido debe ser un objeto JSON.")
        return obj

    def _render_rows(self, rows: list[dict]) -> None:
        for item in self.table.get_children():
            self.table.delete(item)

        for obj in rows:
            key = str(obj.get("id", ""))
            self.table.insert("", tk.END, values=(key, json.dumps(obj, ensure_ascii=False)))

    def refresh_table(self) -> None:
        self._render_rows(self.manager.all_records())

    def on_save(self) -> None:
        try:
            obj = self._read_json_payload()
            id_input = self.id_var.get().strip()
            if id_input:
                obj["id"] = id_input

            inserted = self.manager.save_object(obj)
            if not inserted:
                messagebox.showwarning("Duplicado", "Ya existe un registro con ese ID.")
                return

            messagebox.showinfo("Guardado", "Registro guardado correctamente.")
            self.refresh_table()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def on_find(self) -> None:
        key = self.id_var.get().strip()
        if not key:
            messagebox.showwarning("Atención", "Escribe un ID para buscar.")
            return

        obj = self.manager.find_by_key(key)
        if not obj:
            messagebox.showinfo("Sin resultados", "No se encontró un registro con ese ID.")
            return

        self._render_rows([obj])
        self.json_text.delete("1.0", tk.END)
        self.json_text.insert("1.0", json.dumps(obj, ensure_ascii=False, indent=2))

    def on_update(self) -> None:
        key = self.id_var.get().strip()
        if not key:
            messagebox.showwarning("Atención", "Escribe el ID del registro a actualizar.")
            return

        try:
            obj = self._read_json_payload()
            updated = self.manager.update_object(key, obj)
            if not updated:
                messagebox.showwarning("No existe", "No se encontró el ID para actualizar.")
                return

            messagebox.showinfo("Actualizado", "Registro actualizado correctamente.")
            self.refresh_table()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def on_delete(self) -> None:
        key = self.id_var.get().strip()
        if not key:
            messagebox.showwarning("Atención", "Escribe un ID para eliminar.")
            return

        deleted = self.manager.delete_object(key)
        if not deleted:
            messagebox.showwarning("No existe", "No se encontró un registro con ese ID.")
            return

        messagebox.showinfo("Eliminado", "Registro eliminado correctamente.")
        self.on_clear()
        self.refresh_table()

    def on_query(self) -> None:
        field = self.query_field_var.get()
        value = self.query_value_var.get()
        mode = self.query_mode_var.get()

        results = self.manager.query_by_criteria(field, value, mode)
        self._render_rows(results)

    def on_clear(self) -> None:
        self.id_var.set("")
        self.json_text.delete("1.0", tk.END)
        self.refresh_table()

    def on_select_row(self, _: tk.Event) -> None:
        selected = self.table.selection()
        if not selected:
            return

        values = self.table.item(selected[0], "values")
        if not values:
            return

        self.id_var.set(values[0])
        try:
            parsed = json.loads(values[1])
            self.json_text.delete("1.0", tk.END)
            self.json_text.insert("1.0", json.dumps(parsed, ensure_ascii=False, indent=2))
        except Exception:
            self.json_text.delete("1.0", tk.END)
            self.json_text.insert("1.0", values[1])

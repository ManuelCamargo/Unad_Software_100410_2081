import tkinter as tk
from tkinter import ttk, messagebox
from logger_config import LOG_FILE
from vistas.ui_utils import centrar_ventana


class VentanaLogs(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Software FJ - Eventos y Logs")
        self.transient(master)
        centrar_ventana(self, 900, 560)

        self.crear_interfaz()
        self.cargar_logs()

    def crear_interfaz(self):
        principal = ttk.Frame(self, padding=18)
        principal.pack(fill="both", expand=True)

        ttk.Label(
            principal,
            text="Eventos y errores del sistema",
            style="CardTitle.TLabel"
        ).pack(anchor="w", pady=(0, 12))

        frame_texto = ttk.Frame(principal)
        frame_texto.pack(fill="both", expand=True)

        self.texto = tk.Text(
            frame_texto,
            wrap="none",
            font=("Consolas", 9),
            state="disabled"
        )

        scroll_y = ttk.Scrollbar(frame_texto, orient="vertical", command=self.texto.yview)
        scroll_x = ttk.Scrollbar(frame_texto, orient="horizontal", command=self.texto.xview)

        self.texto.configure(
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        self.texto.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        frame_texto.rowconfigure(0, weight=1)
        frame_texto.columnconfigure(0, weight=1)

        botones = ttk.Frame(principal)
        botones.pack(fill="x", pady=(12, 0))

        ttk.Button(
            botones,
            text="Actualizar",
            command=self.cargar_logs
        ).pack(side="left")

        ttk.Button(
            botones,
            text="Limpiar log",
            command=self.limpiar_log
        ).pack(side="left", padx=8)

        ttk.Button(
            botones,
            text="Cerrar",
            command=self.destroy
        ).pack(side="right")

    def cargar_logs(self):
        contenido = ""

        if LOG_FILE.exists():
            contenido = LOG_FILE.read_text(encoding="utf-8", errors="replace")

        if not contenido:
            contenido = "No hay eventos registrados todavía."

        self.texto.config(state="normal")
        self.texto.delete("1.0", "end")
        self.texto.insert("1.0", contenido)
        self.texto.config(state="disabled")
        self.texto.see("end")

    def limpiar_log(self):
        if messagebox.askyesno(
            "Confirmar",
            "¿Desea borrar el contenido del archivo de log?",
            parent=self
        ):
            LOG_FILE.write_text("", encoding="utf-8")
            self.cargar_logs()

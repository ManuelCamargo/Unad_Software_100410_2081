import tkinter as tk
from tkinter import ttk


def configurar_estilos(root):
    style = ttk.Style(root)

    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure("TLabel", font=("Segoe UI", 10))
    style.configure("TButton", font=("Segoe UI", 10), padding=8)
    style.configure("Heading.TLabel", font=("Segoe UI", 22, "bold"))
    style.configure("Subheading.TLabel", font=("Segoe UI", 11))
    style.configure("CardTitle.TLabel", font=("Segoe UI", 13, "bold"))
    style.configure("Treeview", font=("Segoe UI", 9), rowheight=26)
    style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
    style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), padding=10)


def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    screen_w = ventana.winfo_screenwidth()
    screen_h = ventana.winfo_screenheight()
    x = max((screen_w - ancho) // 2, 0)
    y = max((screen_h - alto) // 2, 0)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

import tkinter as tk
from tkinter import ttk
from vistas.clientes_view import VentanaClientes
from vistas.servicios_view import VentanaServicios
from vistas.reservas_view import VentanaReservas
from vistas.logs_view import VentanaLogs
from vistas.ui_utils import configurar_estilos, centrar_ventana
from logger_config import registrar_evento


class VentanaPrincipal(tk.Tk):
    def __init__(self, almacen):
        super().__init__()
        self.almacen = almacen

        self.title("Software FJ - Sistema Integral de Gestión")
        self.minsize(950, 620)
        centrar_ventana(self, 1050, 680)
        configurar_estilos(self)

        self.protocol("WM_DELETE_WINDOW", self.salir)
        self.crear_menu()
        self.crear_interfaz()
        self.actualizar_resumen()

        registrar_evento("Interfaz gráfica iniciada")

    def crear_menu(self):
        barra = tk.Menu(self)

        menu_archivo = tk.Menu(barra, tearoff=0)
        menu_archivo.add_command(label="Salir", command=self.salir)
        barra.add_cascade(label="Archivo", menu=menu_archivo)

        menu_gestion = tk.Menu(barra, tearoff=0)
        menu_gestion.add_command(label="Clientes", command=self.abrir_clientes)
        menu_gestion.add_command(label="Servicios", command=self.abrir_servicios)
        menu_gestion.add_command(label="Reservas", command=self.abrir_reservas)
        barra.add_cascade(label="Gestión", menu=menu_gestion)

        menu_sistema = tk.Menu(barra, tearoff=0)
        menu_sistema.add_command(label="Ver logs", command=self.abrir_logs)
        barra.add_cascade(label="Sistema", menu=menu_sistema)

        self.config(menu=barra)

    def crear_interfaz(self):
        contenedor = ttk.Frame(self, padding=25)
        contenedor.pack(fill="both", expand=True)

        ttk.Label(
            contenedor,
            text="SOFTWARE FJ",
            style="Heading.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            contenedor,
            text="Sistema Integral de Gestión de Clientes, Servicios y Reservas",
            style="Subheading.TLabel"
        ).pack(anchor="w", pady=(2, 24))

        # Dashboard
        panel_resumen = ttk.Frame(contenedor)
        panel_resumen.pack(fill="x", pady=(0, 28))

        self.card_clientes = self.crear_tarjeta(
            panel_resumen, "Clientes", "0", 0
        )
        self.card_servicios = self.crear_tarjeta(
            panel_resumen, "Servicios", "0", 1
        )
        self.card_reservas = self.crear_tarjeta(
            panel_resumen, "Reservas", "0", 2
        )

        for i in range(3):
            panel_resumen.columnconfigure(i, weight=1)

        ttk.Separator(contenedor).pack(fill="x", pady=(0, 25))

        ttk.Label(
            contenedor,
            text="Módulos",
            style="CardTitle.TLabel"
        ).pack(anchor="w", pady=(0, 14))

        acciones = ttk.Frame(contenedor)
        acciones.pack(fill="both", expand=True)

        botones = [
            ("Gestión de clientes", "Registrar, consultar y eliminar clientes.", self.abrir_clientes),
            ("Gestión de servicios", "Crear salas, equipos y asesorías.", self.abrir_servicios),
            ("Gestión de reservas", "Confirmar, cancelar y calcular costos.", self.abrir_reservas),
            ("Eventos y logs", "Consultar errores y eventos registrados.", self.abrir_logs),
        ]

        for idx, (titulo, descripcion, comando) in enumerate(botones):
            marco = ttk.LabelFrame(acciones, text=titulo, padding=18)
            marco.grid(
                row=idx // 2,
                column=idx % 2,
                padx=8,
                pady=8,
                sticky="nsew"
            )
            ttk.Label(
                marco,
                text=descripcion,
                wraplength=350
            ).pack(anchor="w", pady=(2, 18))
            ttk.Button(
                marco,
                text="Abrir módulo",
                command=comando,
                style="Accent.TButton"
            ).pack(anchor="w")

        for i in range(2):
            acciones.columnconfigure(i, weight=1)
            acciones.rowconfigure(i, weight=1)

        pie = ttk.Label(
            contenedor,
            text="Datos en memoria • Sin base de datos • Manejo de excepciones y logs",
            style="Subheading.TLabel"
        )
        pie.pack(anchor="w", pady=(20, 0))

    def crear_tarjeta(self, padre, titulo, valor, columna):
        frame = ttk.LabelFrame(padre, text=titulo, padding=18)
        frame.grid(row=0, column=columna, padx=8, sticky="ew")
        label = ttk.Label(frame, text=valor, font=("Segoe UI", 25, "bold"))
        label.pack(anchor="center")
        return label

    def actualizar_resumen(self):
        self.card_clientes.config(text=str(len(self.almacen.clientes)))
        self.card_servicios.config(text=str(len(self.almacen.servicios)))
        self.card_reservas.config(text=str(len(self.almacen.reservas)))

    def abrir_clientes(self):
        VentanaClientes(self, self.almacen, self.actualizar_resumen)

    def abrir_servicios(self):
        VentanaServicios(self, self.almacen, self.actualizar_resumen)

    def abrir_reservas(self):
        VentanaReservas(self, self.almacen, self.actualizar_resumen)

    def abrir_logs(self):
        VentanaLogs(self)

    def salir(self):
        registrar_evento("Interfaz gráfica cerrada")
        self.destroy()

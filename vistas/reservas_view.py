import tkinter as tk
from tkinter import ttk, messagebox
from modelos.reserva import Reserva
from modelos.servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from excepciones import ErrorValidacion, ReservaError, ServicioNoDisponibleError
from logger_config import registrar_evento, registrar_error
from vistas.ui_utils import centrar_ventana


class VentanaReservas(tk.Toplevel):
    def __init__(self, master, almacen, callback_actualizar):
        super().__init__(master)
        self.almacen = almacen
        self.callback_actualizar = callback_actualizar

        self.title("Software FJ - Gestión de Reservas")
        self.transient(master)
        centrar_ventana(self, 1050, 690)

        self.crear_interfaz()
        self.actualizar_combobox()
        self.cargar_tabla()

    def crear_interfaz(self):
        principal = ttk.Frame(self, padding=18)
        principal.pack(fill="both", expand=True)

        ttk.Label(
            principal,
            text="Gestión de reservas",
            style="CardTitle.TLabel"
        ).pack(anchor="w", pady=(0, 12))

        formulario = ttk.LabelFrame(principal, text="Nueva reserva", padding=14)
        formulario.pack(fill="x", pady=(0, 15))

        self.codigo = tk.StringVar()
        self.cliente = tk.StringVar()
        self.servicio = tk.StringVar()
        self.duracion = tk.StringVar(value="1")
        self.impuesto = tk.StringVar(value="19")
        self.descuento = tk.StringVar(value="0")
        self.total = tk.StringVar(value="$0")

        ttk.Label(formulario, text="Código reserva").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Entry(formulario, textvariable=self.codigo).grid(row=1, column=0, sticky="ew", padx=5)

        ttk.Label(formulario, text="Cliente").grid(row=0, column=1, sticky="w", padx=5)
        self.cbo_cliente = ttk.Combobox(formulario, textvariable=self.cliente, state="readonly")
        self.cbo_cliente.grid(row=1, column=1, sticky="ew", padx=5)

        ttk.Label(formulario, text="Servicio").grid(row=0, column=2, sticky="w", padx=5)
        self.cbo_servicio = ttk.Combobox(formulario, textvariable=self.servicio, state="readonly")
        self.cbo_servicio.grid(row=1, column=2, sticky="ew", padx=5)

        ttk.Label(formulario, text="Duración (horas)").grid(row=2, column=0, sticky="w", padx=5, pady=(12, 0))
        ttk.Entry(formulario, textvariable=self.duracion).grid(row=3, column=0, sticky="ew", padx=5)

        ttk.Label(formulario, text="IVA (%)").grid(row=2, column=1, sticky="w", padx=5, pady=(12, 0))
        ttk.Entry(formulario, textvariable=self.impuesto).grid(row=3, column=1, sticky="ew", padx=5)

        ttk.Label(formulario, text="Descuento (%)").grid(row=2, column=2, sticky="w", padx=5, pady=(12, 0))
        ttk.Entry(formulario, textvariable=self.descuento).grid(row=3, column=2, sticky="ew", padx=5)

        total_frame = ttk.Frame(formulario)
        total_frame.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(15, 5))

        ttk.Label(total_frame, text="Total calculado:", font=("Segoe UI", 11, "bold")).pack(side="left")
        ttk.Label(total_frame, textvariable=self.total, font=("Segoe UI", 16, "bold")).pack(side="left", padx=10)

        acciones = ttk.Frame(formulario)
        acciones.grid(row=5, column=0, columnspan=3, sticky="w", pady=(8, 0))

        ttk.Button(
            acciones,
            text="Calcular",
            command=self.calcular_total
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            acciones,
            text="Crear y confirmar",
            command=self.crear_reserva,
            style="Accent.TButton"
        ).pack(side="left")

        for i in range(3):
            formulario.columnconfigure(i, weight=1)

        tabla_frame = ttk.LabelFrame(principal, text="Reservas registradas", padding=10)
        tabla_frame.pack(fill="both", expand=True)

        columnas = ("codigo", "cliente", "servicio", "duracion", "estado", "total")
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings")

        headers = {
            "codigo": "Código",
            "cliente": "Cliente",
            "servicio": "Servicio",
            "duracion": "Duración",
            "estado": "Estado",
            "total": "Total base"
        }

        widths = {
            "codigo": 90, "cliente": 190, "servicio": 230,
            "duracion": 90, "estado": 110, "total": 130
        }

        for col in columnas:
            self.tabla.heading(col, text=headers[col])
            self.tabla.column(col, width=widths[col])

        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        pie = ttk.Frame(principal)
        pie.pack(fill="x", pady=(12, 0))

        ttk.Button(
            pie,
            text="Cancelar reserva",
            command=self.cancelar_reserva
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            pie,
            text="Procesar reserva",
            command=self.procesar_reserva
        ).pack(side="left")

        ttk.Button(
            pie,
            text="Actualizar listas",
            command=self.actualizar_combobox
        ).pack(side="left", padx=8)

        ttk.Button(
            pie,
            text="Cerrar",
            command=self.destroy
        ).pack(side="right")

    def actualizar_combobox(self):
        self.cbo_cliente["values"] = [
            f"{c.codigo} | {c.nombre}" for c in self.almacen.clientes
        ]

        self.cbo_servicio["values"] = [
            f"{s.codigo} | {s.nombre}" for s in self.almacen.servicios
        ]

    def obtener_cliente(self):
        valor = self.cliente.get()
        if not valor:
            raise ErrorValidacion("Debe seleccionar un cliente.")
        codigo = valor.split("|")[0].strip()
        cliente = self.almacen.buscar_cliente(codigo)
        if not cliente:
            raise ErrorValidacion("El cliente seleccionado ya no existe.")
        return cliente

    def obtener_servicio(self):
        valor = self.servicio.get()
        if not valor:
            raise ErrorValidacion("Debe seleccionar un servicio.")
        codigo = valor.split("|")[0].strip()
        servicio = self.almacen.buscar_servicio(codigo)
        if not servicio:
            raise ErrorValidacion("El servicio seleccionado ya no existe.")
        return servicio

    def leer_numeros(self):
        try:
            duracion = float(self.duracion.get().replace(",", "."))
            impuesto = float(self.impuesto.get().replace(",", ".")) / 100
            descuento = float(self.descuento.get().replace(",", ".")) / 100
        except ValueError as error:
            raise ErrorValidacion(
                "Duración, IVA y descuento deben ser valores numéricos."
            ) from error

        return duracion, impuesto, descuento

    def crear_reserva_temporal(self):
        cliente = self.obtener_cliente()
        servicio = self.obtener_servicio()
        duracion, impuesto, descuento = self.leer_numeros()

        codigo = self.codigo.get().strip() or "TEMP"

        reserva = Reserva(
            codigo,
            cliente,
            servicio,
            duracion
        )

        return reserva, impuesto, descuento

    def calcular_total(self):
        try:
            reserva, impuesto, descuento = self.crear_reserva_temporal()
            total = reserva.calcular_total(
                impuesto=impuesto,
                descuento=descuento
            )

        except (ErrorValidacion, ReservaError, ServicioNoDisponibleError) as error:
            registrar_error(f"Error al calcular reserva: {error}")
            messagebox.showerror("Error", str(error), parent=self)

        except Exception as error:
            registrar_error(f"Error inesperado al calcular reserva: {error}")
            messagebox.showerror(
                "Error inesperado",
                "No fue posible calcular la reserva.",
                parent=self
            )

        else:
            self.total.set(f"${total:,.0f}")

        finally:
            self.focus_set()

    def crear_reserva(self):
        try:
            codigo = self.codigo.get().strip()

            if not codigo:
                raise ErrorValidacion("El código de la reserva es obligatorio.")

            if self.almacen.codigo_reserva_existe(codigo):
                raise ErrorValidacion(f"Ya existe una reserva con código {codigo}.")

            reserva, impuesto, descuento = self.crear_reserva_temporal()
            reserva.confirmar()

            total = reserva.calcular_total(
                impuesto=impuesto,
                descuento=descuento
            )

        except (ErrorValidacion, ReservaError, ServicioNoDisponibleError) as error:
            registrar_error(f"Error al crear reserva: {error}")
            messagebox.showerror("Error de reserva", str(error), parent=self)

        except Exception as error:
            registrar_error(f"Error inesperado al crear reserva: {error}")
            messagebox.showerror(
                "Error inesperado",
                "No fue posible crear la reserva.",
                parent=self
            )

        else:
            self.almacen.reservas.append(reserva)
            registrar_evento(
                f"Reserva confirmada: {reserva.codigo} - "
                f"{reserva.cliente.nombre} - {reserva.servicio.nombre}"
            )
            self.total.set(f"${total:,.0f}")
            self.cargar_tabla()
            self.callback_actualizar()

            messagebox.showinfo(
                "Software FJ",
                f"Reserva confirmada correctamente.\nTotal: ${total:,.0f}",
                parent=self
            )

        finally:
            self.focus_set()

    def obtener_reserva_seleccionada(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning(
                "Software FJ",
                "Seleccione una reserva.",
                parent=self
            )
            return None

        codigo = self.tabla.item(seleccion[0], "values")[0]
        return self.almacen.buscar_reserva(codigo)

    def cancelar_reserva(self):
        reserva = self.obtener_reserva_seleccionada()
        if not reserva:
            return

        try:
            reserva.cancelar()
        except ReservaError as error:
            registrar_error(f"Error al cancelar reserva {reserva.codigo}: {error}")
            messagebox.showerror("Error", str(error), parent=self)
        else:
            registrar_evento(f"Reserva cancelada: {reserva.codigo}")
            self.cargar_tabla()

    def procesar_reserva(self):
        reserva = self.obtener_reserva_seleccionada()
        if not reserva:
            return

        try:
            reserva.procesar()
        except ReservaError as error:
            registrar_error(f"Error al procesar reserva {reserva.codigo}: {error}")
            messagebox.showerror("Error", str(error), parent=self)
        else:
            registrar_evento(f"Reserva procesada: {reserva.codigo}")
            self.cargar_tabla()

    def cargar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for reserva in self.almacen.reservas:
            try:
                total = reserva.calcular_total()
                total_txt = f"${total:,.0f}"
            except Exception:
                total_txt = "Error"

            self.tabla.insert(
                "",
                "end",
                values=(
                    reserva.codigo,
                    reserva.cliente.nombre,
                    reserva.servicio.nombre,
                    f"{reserva.duracion:g} h",
                    reserva.estado,
                    total_txt
                )
            )

import tkinter as tk
from tkinter import ttk, messagebox
from modelos.servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from excepciones import ErrorValidacion
from logger_config import registrar_evento, registrar_error
from vistas.ui_utils import centrar_ventana


class VentanaServicios(tk.Toplevel):
    TIPOS = ("Reserva de sala", "Alquiler de equipo", "Asesoría especializada")

    def __init__(self, master, almacen, callback_actualizar):
        super().__init__(master)
        self.almacen = almacen
        self.callback_actualizar = callback_actualizar

        self.title("Software FJ - Gestión de Servicios")
        self.transient(master)
        centrar_ventana(self, 980, 650)

        self.crear_interfaz()
        self.cargar_tabla()

    def crear_interfaz(self):
        principal = ttk.Frame(self, padding=18)
        principal.pack(fill="both", expand=True)

        ttk.Label(
            principal,
            text="Gestión de servicios",
            style="CardTitle.TLabel"
        ).pack(anchor="w", pady=(0, 12))

        formulario = ttk.LabelFrame(principal, text="Nuevo servicio", padding=14)
        formulario.pack(fill="x", pady=(0, 15))

        self.codigo = tk.StringVar()
        self.nombre = tk.StringVar()
        self.precio = tk.StringVar()
        self.tipo = tk.StringVar(value=self.TIPOS[0])
        self.extra = tk.StringVar()

        ttk.Label(formulario, text="Código").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Entry(formulario, textvariable=self.codigo).grid(row=1, column=0, sticky="ew", padx=5)

        ttk.Label(formulario, text="Nombre").grid(row=0, column=1, sticky="w", padx=5)
        ttk.Entry(formulario, textvariable=self.nombre).grid(row=1, column=1, sticky="ew", padx=5)

        ttk.Label(formulario, text="Precio base / hora").grid(row=0, column=2, sticky="w", padx=5)
        ttk.Entry(formulario, textvariable=self.precio).grid(row=1, column=2, sticky="ew", padx=5)

        ttk.Label(formulario, text="Tipo").grid(row=2, column=0, sticky="w", padx=5, pady=(12, 0))
        combo = ttk.Combobox(
            formulario,
            textvariable=self.tipo,
            values=self.TIPOS,
            state="readonly"
        )
        combo.grid(row=3, column=0, sticky="ew", padx=5)
        combo.bind("<<ComboboxSelected>>", lambda e: self.actualizar_campo_extra())

        self.lbl_extra = ttk.Label(formulario, text="Capacidad")
        self.lbl_extra.grid(row=2, column=1, sticky="w", padx=5, pady=(12, 0))
        ttk.Entry(formulario, textvariable=self.extra).grid(row=3, column=1, sticky="ew", padx=5)

        ttk.Button(
            formulario,
            text="Guardar servicio",
            command=self.guardar_servicio,
            style="Accent.TButton"
        ).grid(row=3, column=2, sticky="ew", padx=5)

        for i in range(3):
            formulario.columnconfigure(i, weight=1)

        tabla_frame = ttk.LabelFrame(principal, text="Servicios registrados", padding=10)
        tabla_frame.pack(fill="both", expand=True)

        columnas = ("codigo", "tipo", "nombre", "precio", "detalle", "estado")
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings")

        headers = {
            "codigo": "Código",
            "tipo": "Tipo",
            "nombre": "Nombre",
            "precio": "Precio/hora",
            "detalle": "Detalle",
            "estado": "Disponible",
        }

        widths = {
            "codigo": 80, "tipo": 150, "nombre": 190,
            "precio": 110, "detalle": 170, "estado": 90
        }

        for col in columnas:
            self.tabla.heading(col, text=headers[col])
            self.tabla.column(col, width=widths[col])

        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        acciones = ttk.Frame(principal)
        acciones.pack(fill="x", pady=(12, 0))

        ttk.Button(
            acciones,
            text="Cambiar disponibilidad",
            command=self.cambiar_disponibilidad
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            acciones,
            text="Eliminar seleccionado",
            command=self.eliminar_servicio
        ).pack(side="left")

        ttk.Button(
            acciones,
            text="Cerrar",
            command=self.destroy
        ).pack(side="right")

    def actualizar_campo_extra(self):
        tipo = self.tipo.get()

        if tipo == "Reserva de sala":
            texto = "Capacidad"
        elif tipo == "Alquiler de equipo":
            texto = "Cantidad disponible"
        else:
            texto = "Especialidad"

        self.lbl_extra.config(text=texto)
        self.extra.set("")

    def guardar_servicio(self):
        try:
            codigo = self.codigo.get().strip()

            if self.almacen.codigo_servicio_existe(codigo):
                raise ErrorValidacion(f"Ya existe un servicio con código {codigo}.")

            try:
                precio = float(self.precio.get().replace(",", "."))
            except ValueError as error:
                raise ErrorValidacion("El precio debe ser numérico.") from error

            tipo = self.tipo.get()

            if tipo == "Reserva de sala":
                try:
                    capacidad = int(self.extra.get())
                except ValueError as error:
                    raise ErrorValidacion("La capacidad debe ser un número entero.") from error

                servicio = ReservaSala(
                    codigo,
                    self.nombre.get(),
                    precio,
                    capacidad
                )

            elif tipo == "Alquiler de equipo":
                try:
                    cantidad = int(self.extra.get())
                except ValueError as error:
                    raise ErrorValidacion("La cantidad debe ser un número entero.") from error

                servicio = AlquilerEquipo(
                    codigo,
                    self.nombre.get(),
                    precio,
                    cantidad
                )

            else:
                servicio = AsesoriaEspecializada(
                    codigo,
                    self.nombre.get(),
                    precio,
                    self.extra.get()
                )

        except ErrorValidacion as error:
            registrar_error(f"Error al crear servicio: {error}")
            messagebox.showerror("Error de validación", str(error), parent=self)

        except Exception as error:
            registrar_error(f"Error inesperado al crear servicio: {error}")
            messagebox.showerror(
                "Error inesperado",
                "No fue posible crear el servicio.",
                parent=self
            )

        else:
            self.almacen.servicios.append(servicio)
            registrar_evento(f"Servicio registrado: {servicio.codigo} - {servicio.nombre}")
            self.limpiar()
            self.cargar_tabla()
            self.callback_actualizar()

            messagebox.showinfo(
                "Software FJ",
                "Servicio registrado correctamente.",
                parent=self
            )

        finally:
            self.focus_set()

    def detalle_servicio(self, servicio):
        if isinstance(servicio, ReservaSala):
            return f"Capacidad: {servicio.capacidad}"
        if isinstance(servicio, AlquilerEquipo):
            return f"Disponibles: {servicio.cantidad_disponible}"
        return f"Especialidad: {servicio.especialidad}"

    def tipo_servicio(self, servicio):
        if isinstance(servicio, ReservaSala):
            return "Reserva de sala"
        if isinstance(servicio, AlquilerEquipo):
            return "Alquiler de equipo"
        return "Asesoría especializada"

    def cargar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for servicio in self.almacen.servicios:
            self.tabla.insert(
                "",
                "end",
                values=(
                    servicio.codigo,
                    self.tipo_servicio(servicio),
                    servicio.nombre,
                    f"${servicio._precio_base:,.0f}",
                    self.detalle_servicio(servicio),
                    "Sí" if servicio.disponible else "No"
                )
            )

    def obtener_servicio_seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Software FJ", "Seleccione un servicio.", parent=self)
            return None

        codigo = self.tabla.item(seleccion[0], "values")[0]
        return self.almacen.buscar_servicio(codigo)

    def cambiar_disponibilidad(self):
        servicio = self.obtener_servicio_seleccionado()
        if not servicio:
            return

        servicio.cambiar_disponibilidad(not servicio.disponible)
        registrar_evento(
            f"Disponibilidad cambiada: {servicio.codigo} -> {servicio.disponible}"
        )
        self.cargar_tabla()

    def eliminar_servicio(self):
        servicio = self.obtener_servicio_seleccionado()
        if not servicio:
            return

        usado = any(r.servicio.codigo == servicio.codigo for r in self.almacen.reservas)
        if usado:
            messagebox.showwarning(
                "Operación no permitida",
                "El servicio tiene reservas asociadas y no puede eliminarse.",
                parent=self
            )
            return

        if messagebox.askyesno(
            "Confirmar",
            f"¿Eliminar el servicio {servicio.nombre}?",
            parent=self
        ):
            self.almacen.servicios.remove(servicio)
            registrar_evento(f"Servicio eliminado: {servicio.codigo}")
            self.cargar_tabla()
            self.callback_actualizar()

    def limpiar(self):
        self.codigo.set("")
        self.nombre.set("")
        self.precio.set("")
        self.extra.set("")

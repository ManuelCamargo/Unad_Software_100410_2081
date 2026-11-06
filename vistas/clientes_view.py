import tkinter as tk
from tkinter import ttk, messagebox
from modelos.cliente import Cliente
from excepciones import ErrorValidacion
from logger_config import registrar_evento, registrar_error
from vistas.ui_utils import centrar_ventana


class VentanaClientes(tk.Toplevel):
    def __init__(self, master, almacen, callback_actualizar):
        super().__init__(master)
        self.almacen = almacen
        self.callback_actualizar = callback_actualizar

        self.title("Software FJ - Gestión de Clientes")
        self.transient(master)
        centrar_ventana(self, 930, 580)

        self.crear_interfaz()
        self.cargar_tabla()

    def crear_interfaz(self):
        principal = ttk.Frame(self, padding=18)
        principal.pack(fill="both", expand=True)

        ttk.Label(
            principal,
            text="Gestión de clientes",
            style="CardTitle.TLabel"
        ).pack(anchor="w", pady=(0, 12))

        formulario = ttk.LabelFrame(principal, text="Nuevo cliente", padding=14)
        formulario.pack(fill="x", pady=(0, 15))

        campos = [
            ("Código", "codigo"),
            ("Nombre", "nombre"),
            ("Correo", "correo"),
            ("Teléfono", "telefono"),
        ]

        self.vars = {}
        for col, (label, key) in enumerate(campos):
            ttk.Label(formulario, text=label).grid(row=0, column=col, padx=6, pady=3, sticky="w")
            var = tk.StringVar()
            self.vars[key] = var
            ttk.Entry(formulario, textvariable=var, width=24).grid(
                row=1, column=col, padx=6, pady=3, sticky="ew"
            )
            formulario.columnconfigure(col, weight=1)

        botones = ttk.Frame(formulario)
        botones.grid(row=2, column=0, columnspan=4, sticky="w", pady=(12, 0))

        ttk.Button(
            botones,
            text="Guardar cliente",
            command=self.guardar_cliente,
            style="Accent.TButton"
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            botones,
            text="Limpiar",
            command=self.limpiar_formulario
        ).pack(side="left")

        tabla_frame = ttk.LabelFrame(principal, text="Clientes registrados", padding=10)
        tabla_frame.pack(fill="both", expand=True)

        columnas = ("codigo", "nombre", "correo", "telefono")
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings")

        self.tabla.heading("codigo", text="Código")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("correo", text="Correo")
        self.tabla.heading("telefono", text="Teléfono")

        self.tabla.column("codigo", width=90)
        self.tabla.column("nombre", width=210)
        self.tabla.column("correo", width=270)
        self.tabla.column("telefono", width=150)

        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        acciones = ttk.Frame(principal)
        acciones.pack(fill="x", pady=(12, 0))

        ttk.Button(
            acciones,
            text="Eliminar seleccionado",
            command=self.eliminar_cliente
        ).pack(side="left")

        ttk.Button(
            acciones,
            text="Cerrar",
            command=self.destroy
        ).pack(side="right")

    def guardar_cliente(self):
        try:
            codigo = self.vars["codigo"].get().strip()

            if self.almacen.codigo_cliente_existe(codigo):
                raise ErrorValidacion(f"Ya existe un cliente con código {codigo}.")

            cliente = Cliente(
                codigo,
                self.vars["nombre"].get(),
                self.vars["correo"].get(),
                self.vars["telefono"].get()
            )

        except ErrorValidacion as error:
            registrar_error(f"Error al crear cliente: {error}")
            messagebox.showerror("Error de validación", str(error), parent=self)

        except Exception as error:
            registrar_error(f"Error inesperado al crear cliente: {error}")
            messagebox.showerror(
                "Error inesperado",
                "No fue posible registrar el cliente.",
                parent=self
            )

        else:
            self.almacen.clientes.append(cliente)
            registrar_evento(f"Cliente registrado: {cliente.codigo} - {cliente.nombre}")
            self.cargar_tabla()
            self.limpiar_formulario()
            self.callback_actualizar()

            messagebox.showinfo(
                "Software FJ",
                "Cliente registrado correctamente.",
                parent=self
            )

        finally:
            self.focus_set()

    def eliminar_cliente(self):
        seleccion = self.tabla.selection()

        if not seleccion:
            messagebox.showwarning(
                "Software FJ",
                "Seleccione un cliente.",
                parent=self
            )
            return

        codigo = self.tabla.item(seleccion[0], "values")[0]

        usado = any(r.cliente.codigo == codigo for r in self.almacen.reservas)
        if usado:
            messagebox.showwarning(
                "Operación no permitida",
                "El cliente tiene reservas asociadas y no puede eliminarse.",
                parent=self
            )
            return

        cliente = self.almacen.buscar_cliente(codigo)

        if cliente and messagebox.askyesno(
            "Confirmar",
            f"¿Eliminar al cliente {cliente.nombre}?",
            parent=self
        ):
            self.almacen.clientes.remove(cliente)
            registrar_evento(f"Cliente eliminado: {codigo}")
            self.cargar_tabla()
            self.callback_actualizar()

    def limpiar_formulario(self):
        for var in self.vars.values():
            var.set("")

    def cargar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for cliente in self.almacen.clientes:
            self.tabla.insert(
                "",
                "end",
                values=(
                    cliente.codigo,
                    cliente.nombre,
                    cliente.correo,
                    cliente.telefono
                )
            )

from datos import AlmacenDatos
from modelos.cliente import Cliente
from modelos.servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from modelos.reserva import Reserva
from vistas.ventana_principal import VentanaPrincipal


def cargar_datos_demostracion(almacen):
    cliente1 = Cliente("1001", "Ana Torres", "ana@correo.com", "3001234567")
    cliente2 = Cliente("1002", "Carlos Ruiz", "carlos@correo.com", "3104567890")
    almacen.clientes.extend([cliente1, cliente2])

    sala = ReservaSala("S001", "Sala de reuniones", 50000, capacidad=12)
    equipo = AlquilerEquipo("S002", "Portátil empresarial", 35000, cantidad_disponible=3)
    asesoria = AsesoriaEspecializada("S003", "Asesoría en Python", 80000, "Programación")
    almacen.servicios.extend([sala, equipo, asesoria])

    reserva = Reserva("R001", cliente1, sala, 2)
    reserva.confirmar()
    almacen.reservas.append(reserva)


if __name__ == "__main__":
    almacen = AlmacenDatos()
    cargar_datos_demostracion(almacen)

    app = VentanaPrincipal(almacen)
    app.mainloop()

"""
Proyecto Fase 4 - Programación 213023
Sistema Integral de Gestión de Clientes, Servicios y Reservas
Empresa simulada: Software FJ
"""

from modelos.cliente import Cliente
from modelos.servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from modelos.reserva import Reserva
from excepciones import ErrorValidacion, ServicioNoDisponibleError, ReservaError
from logger_config import registrar_evento, registrar_error


def ejecutar_operacion(numero, descripcion, funcion):
    """Ejecuta una operación controlando los errores sin detener el programa."""
    print(f"\n{'=' * 65}")
    print(f"OPERACIÓN {numero}: {descripcion}")
    print("=" * 65)

    try:
        resultado = funcion()
    except (ErrorValidacion, ServicioNoDisponibleError, ReservaError) as error:
        print(f"ERROR CONTROLADO: {error}")
        registrar_error(f"Operación {numero} - {descripcion}: {error}")
    except Exception as error:
        print(f"ERROR INESPERADO: {error}")
        registrar_error(f"Error inesperado en operación {numero}: {error}")
    else:
        if resultado is not None:
            print(resultado)
        registrar_evento(f"Operación {numero} completada: {descripcion}")
    finally:
        print(f"Fin de la operación {numero}.")


def main():
    print("\nSOFTWARE FJ")
    print("Sistema Integral de Gestión de Clientes, Servicios y Reservas")
    registrar_evento("Inicio de la aplicación")

    clientes = []
    servicios = []
    reservas = []

    # 1. Cliente válido
    def op1():
        cliente = Cliente("1001", "Ana Torres", "ana@correo.com", "3001234567")
        clientes.append(cliente)
        return f"Cliente creado: {cliente}"

    ejecutar_operacion(1, "Registrar cliente válido", op1)

    # 2. Cliente inválido: nombre vacío
    ejecutar_operacion(
        2,
        "Intentar registrar cliente con nombre vacío",
        lambda: Cliente("1002", "", "sin_nombre@correo.com", "3001112233")
    )

    # 3. Cliente inválido: correo
    ejecutar_operacion(
        3,
        "Intentar registrar cliente con correo inválido",
        lambda: Cliente("1003", "Pedro López", "correo-invalido", "3002223344")
    )

    # 4. Crear servicio de sala
    def op4():
        servicio = ReservaSala("S001", "Sala de reuniones", 50000, capacidad=12)
        servicios.append(servicio)
        return f"Servicio creado: {servicio.descripcion()}"

    ejecutar_operacion(4, "Crear servicio de reserva de sala", op4)

    # 5. Crear alquiler de equipo
    def op5():
        servicio = AlquilerEquipo("S002", "Portátil empresarial", 35000, cantidad_disponible=3)
        servicios.append(servicio)
        return f"Servicio creado: {servicio.descripcion()}"

    ejecutar_operacion(5, "Crear servicio de alquiler de equipo", op5)

    # 6. Crear asesoría
    def op6():
        servicio = AsesoriaEspecializada("S003", "Asesoría en Python", 80000, especialidad="Programación")
        servicios.append(servicio)
        return f"Servicio creado: {servicio.descripcion()}"

    ejecutar_operacion(6, "Crear servicio de asesoría especializada", op6)

    # 7. Servicio inválido: precio negativo
    ejecutar_operacion(
        7,
        "Intentar crear servicio con precio negativo",
        lambda: ReservaSala("S004", "Sala inválida", -20000, capacidad=5)
    )

    # 8. Reserva exitosa
    def op8():
        reserva = Reserva("R001", clientes[0], servicios[0], duracion=2)
        reserva.confirmar()
        reservas.append(reserva)
        return (
            f"Reserva confirmada: {reserva}\n"
            f"Costo base: ${reserva.calcular_total():,.0f}\n"
            f"Costo con IVA 19%: ${reserva.calcular_total(impuesto=0.19):,.0f}"
        )

    ejecutar_operacion(8, "Crear y confirmar una reserva válida", op8)

    # 9. Reserva inválida: duración 0
    ejecutar_operacion(
        9,
        "Intentar crear reserva con duración igual a cero",
        lambda: Reserva("R002", clientes[0], servicios[1], duracion=0)
    )

    # 10. Reserva de más equipos que los disponibles
    def op10():
        equipo = servicios[1]
        equipo.validar_parametros(cantidad=10)
        return "La cantidad solicitada está disponible."

    ejecutar_operacion(10, "Solicitar más equipos que los disponibles", op10)

    # 11. Cálculo con descuento
    def op11():
        reserva = Reserva("R003", clientes[0], servicios[2], duracion=3)
        reserva.confirmar()
        reservas.append(reserva)
        return (
            f"Reserva de asesoría confirmada.\n"
            f"Total normal: ${reserva.calcular_total():,.0f}\n"
            f"Total con descuento 10%: ${reserva.calcular_total(descuento=0.10):,.0f}"
        )

    ejecutar_operacion(11, "Calcular reserva con descuento", op11)

    # 12. Cancelar reserva
    def op12():
        reserva = reservas[0]
        reserva.cancelar()
        return f"Reserva {reserva.codigo} cancelada correctamente."

    ejecutar_operacion(12, "Cancelar una reserva confirmada", op12)

    print("\n" + "=" * 65)
    print("RESUMEN")
    print("=" * 65)
    print(f"Clientes almacenados en memoria: {len(clientes)}")
    print(f"Servicios almacenados en memoria: {len(servicios)}")
    print(f"Reservas almacenadas en memoria: {len(reservas)}")
    print("El programa terminó sin interrumpirse por los errores simulados.")
    print("Revise el archivo logs/software_fj.log para consultar eventos y errores.")
    registrar_evento("Fin de la aplicación")


if __name__ == "__main__":
    main()

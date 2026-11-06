from modelos.entidad import Entidad
from modelos.cliente import Cliente
from modelos.servicio import Servicio
from excepciones import ErrorValidacion, ReservaError


class Reserva(Entidad):
    """Integra un cliente, un servicio, duración y estado de la reserva."""

    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA")

    def __init__(self, codigo, cliente, servicio, duracion):
        try:
            super().__init__(codigo)
        except ValueError as error:
            raise ErrorValidacion("El código de la reserva es obligatorio.") from error

        if not isinstance(cliente, Cliente):
            raise ErrorValidacion("La reserva requiere un cliente válido.")

        if not isinstance(servicio, Servicio):
            raise ErrorValidacion("La reserva requiere un servicio válido.")

        if duracion <= 0:
            raise ErrorValidacion("La duración de la reserva debe ser mayor que cero.")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "PENDIENTE"

    def confirmar(self):
        if self.estado != "PENDIENTE":
            raise ReservaError(
                f"No se puede confirmar una reserva en estado {self.estado}."
            )

        try:
            self.servicio.verificar_disponibilidad()
        except Exception as error:
            raise ReservaError(
                "No fue posible confirmar la reserva porque el servicio no está disponible."
            ) from error

        self.estado = "CONFIRMADA"

    def cancelar(self):
        if self.estado == "CANCELADA":
            raise ReservaError("La reserva ya se encuentra cancelada.")

        if self.estado == "PROCESADA":
            raise ReservaError("No se puede cancelar una reserva procesada.")

        self.estado = "CANCELADA"

    def procesar(self):
        if self.estado != "CONFIRMADA":
            raise ReservaError("Solo se pueden procesar reservas confirmadas.")
        self.estado = "PROCESADA"

    def calcular_total(self, impuesto=0.0, descuento=0.0):
        """
        En Python no existe sobrecarga tradicional como en otros lenguajes.
        Se simula usando parámetros opcionales:
        - calcular_total()
        - calcular_total(impuesto=0.19)
        - calcular_total(descuento=0.10)
        - calcular_total(impuesto=0.19, descuento=0.10)
        """
        if impuesto < 0:
            raise ErrorValidacion("El impuesto no puede ser negativo.")

        if descuento < 0 or descuento > 1:
            raise ErrorValidacion("El descuento debe estar entre 0 y 1.")

        try:
            subtotal = self.servicio.calcular_costo(self.duracion)
            subtotal -= subtotal * descuento
            total = subtotal + (subtotal * impuesto)
        except (TypeError, ValueError) as error:
            raise ReservaError("No fue posible calcular el costo de la reserva.") from error

        return total

    def descripcion(self):
        return (
            f"Reserva {self.codigo}: {self.cliente.nombre} - "
            f"{self.servicio.nombre} - {self.estado}"
        )

    def __str__(self):
        return (
            f"{self.codigo} | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Duración: {self.duracion} hora(s) | Estado: {self.estado}"
        )

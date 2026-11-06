class SoftwareFJError(Exception):
    """Excepción base del sistema Software FJ."""


class ErrorValidacion(SoftwareFJError):
    """Se genera cuando un dato no cumple las reglas de validación."""


class ServicioNoDisponibleError(SoftwareFJError):
    """Se genera cuando un servicio no está disponible."""


class ReservaError(SoftwareFJError):
    """Se genera cuando una operación de reserva no es válida."""

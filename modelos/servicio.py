from abc import abstractmethod
from modelos.entidad import Entidad
from excepciones import ErrorValidacion, ServicioNoDisponibleError


class Servicio(Entidad):
    """Clase abstracta para todos los servicios ofrecidos por Software FJ."""

    def __init__(self, codigo, nombre, precio_base):
        try:
            super().__init__(codigo)
        except ValueError as error:
            raise ErrorValidacion("El código del servicio es obligatorio.") from error

        if not nombre or len(nombre.strip()) < 3:
            raise ErrorValidacion("El nombre del servicio no es válido.")

        if precio_base <= 0:
            raise ErrorValidacion("El precio base debe ser mayor que cero.")

        self._nombre = nombre.strip()
        self._precio_base = float(precio_base)
        self._disponible = True

    @property
    def nombre(self):
        return self._nombre

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, disponible):
        self._disponible = bool(disponible)

    def verificar_disponibilidad(self):
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.nombre}' no se encuentra disponible."
            )

    @abstractmethod
    def calcular_costo(self, duracion):
        pass

    @abstractmethod
    def validar_parametros(self, **kwargs):
        pass


class ReservaSala(Servicio):
    """Servicio para reservar salas por horas."""

    def __init__(self, codigo, nombre, precio_base, capacidad):
        super().__init__(codigo, nombre, precio_base)
        if capacidad <= 0:
            raise ErrorValidacion("La capacidad de la sala debe ser mayor que cero.")
        self.capacidad = capacidad

    def calcular_costo(self, duracion):
        self.verificar_disponibilidad()
        if duracion <= 0:
            raise ErrorValidacion("La duración debe ser mayor que cero.")
        return self._precio_base * duracion

    def validar_parametros(self, **kwargs):
        asistentes = kwargs.get("asistentes", 1)
        if asistentes <= 0:
            raise ErrorValidacion("Debe existir por lo menos un asistente.")
        if asistentes > self.capacidad:
            raise ServicioNoDisponibleError(
                f"La sala solo admite {self.capacidad} personas."
            )
        return True

    def descripcion(self):
        return (
            f"{self.nombre} | Reserva de sala | "
            f"Capacidad: {self.capacidad} | Precio/hora: ${self._precio_base:,.0f}"
        )


class AlquilerEquipo(Servicio):
    """Servicio para alquiler de equipos."""

    def __init__(self, codigo, nombre, precio_base, cantidad_disponible):
        super().__init__(codigo, nombre, precio_base)
        if cantidad_disponible < 0:
            raise ErrorValidacion("La cantidad disponible no puede ser negativa.")
        self.cantidad_disponible = cantidad_disponible

    def calcular_costo(self, duracion):
        self.verificar_disponibilidad()
        if duracion <= 0:
            raise ErrorValidacion("La duración debe ser mayor que cero.")
        return self._precio_base * duracion

    def validar_parametros(self, **kwargs):
        cantidad = kwargs.get("cantidad", 1)

        if cantidad <= 0:
            raise ErrorValidacion("La cantidad solicitada debe ser mayor que cero.")

        if cantidad > self.cantidad_disponible:
            raise ServicioNoDisponibleError(
                f"Solo hay {self.cantidad_disponible} equipo(s) disponible(s)."
            )
        return True

    def descripcion(self):
        return (
            f"{self.nombre} | Alquiler de equipo | "
            f"Disponibles: {self.cantidad_disponible} | Precio/hora: ${self._precio_base:,.0f}"
        )


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría profesional especializada."""

    def __init__(self, codigo, nombre, precio_base, especialidad):
        super().__init__(codigo, nombre, precio_base)

        if not especialidad or len(especialidad.strip()) < 3:
            raise ErrorValidacion("La especialidad es obligatoria.")

        self.especialidad = especialidad.strip()

    def calcular_costo(self, duracion):
        self.verificar_disponibilidad()
        if duracion <= 0:
            raise ErrorValidacion("La duración debe ser mayor que cero.")
        return self._precio_base * duracion

    def validar_parametros(self, **kwargs):
        modalidad = kwargs.get("modalidad", "virtual").lower()

        if modalidad not in ("virtual", "presencial"):
            raise ErrorValidacion(
                "La modalidad debe ser 'virtual' o 'presencial'."
            )
        return True

    def descripcion(self):
        return (
            f"{self.nombre} | Asesoría especializada en {self.especialidad} | "
            f"Precio/hora: ${self._precio_base:,.0f}"
        )

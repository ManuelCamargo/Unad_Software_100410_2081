from abc import ABC, abstractmethod


class Entidad(ABC):
    """Clase abstracta general para las entidades del sistema."""

    def __init__(self, codigo):
        if not codigo or not str(codigo).strip():
            raise ValueError("El código de la entidad es obligatorio.")
        self._codigo = str(codigo).strip()

    @property
    def codigo(self):
        return self._codigo

    @abstractmethod
    def descripcion(self):
        """Cada clase derivada debe describirse a sí misma."""
        pass

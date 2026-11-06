import re
from modelos.entidad import Entidad
from excepciones import ErrorValidacion


class Cliente(Entidad):
    """Representa un cliente con datos encapsulados y validados."""

    def __init__(self, codigo, nombre, correo, telefono):
        try:
            super().__init__(codigo)
        except ValueError as error:
            raise ErrorValidacion("El código del cliente es obligatorio.") from error

        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or len(valor.strip()) < 3:
            raise ErrorValidacion("El nombre debe tener al menos 3 caracteres.")
        self.__nombre = valor.strip()

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not valor or not re.match(patron, valor):
            raise ErrorValidacion("El correo electrónico no es válido.")
        self.__correo = valor.strip().lower()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        telefono = str(valor).strip()
        if not telefono.isdigit() or len(telefono) < 7:
            raise ErrorValidacion("El teléfono debe ser numérico y tener mínimo 7 dígitos.")
        self.__telefono = telefono

    def descripcion(self):
        return f"Cliente {self.nombre} - {self.correo}"

    def __str__(self):
        return f"{self.codigo} | {self.nombre} | {self.correo} | {self.telefono}"

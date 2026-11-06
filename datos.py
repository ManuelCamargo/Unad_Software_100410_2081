class AlmacenDatos:
    """Almacén temporal en memoria. No utiliza base de datos."""

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def buscar_cliente(self, codigo):
        return next((c for c in self.clientes if c.codigo == codigo), None)

    def buscar_servicio(self, codigo):
        return next((s for s in self.servicios if s.codigo == codigo), None)

    def buscar_reserva(self, codigo):
        return next((r for r in self.reservas if r.codigo == codigo), None)

    def codigo_cliente_existe(self, codigo):
        return self.buscar_cliente(codigo) is not None

    def codigo_servicio_existe(self, codigo):
        return self.buscar_servicio(codigo) is not None

    def codigo_reserva_existe(self, codigo):
        return self.buscar_reserva(codigo) is not None

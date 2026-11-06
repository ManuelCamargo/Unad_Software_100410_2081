from datos import AlmacenDatos
from vistas.ventana_principal import VentanaPrincipal


def main():
    almacen = AlmacenDatos()
    app = VentanaPrincipal(almacen)
    app.mainloop()


if __name__ == "__main__":
    main()

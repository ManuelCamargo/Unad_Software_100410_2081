# Software FJ - Fase 4

Sistema Integral de Gestión de Clientes, Servicios y Reservas desarrollado en Python con programación orientada a objetos y una interfaz gráfica en Tkinter.

## Requisitos académicos implementados

- Clase abstracta general.
- Clase `Cliente` con validaciones y encapsulación.
- Clase abstracta `Servicio`.
- Tres servicios derivados:
  - Reserva de sala.
  - Alquiler de equipo.
  - Asesoría especializada.
- Clase `Reserva`.
- Herencia.
- Polimorfismo.
- Encapsulación.
- Métodos sobrescritos.
- Parámetros opcionales para cálculo con impuesto y descuento.
- Excepciones personalizadas.
- `try/except`.
- `try/except/else`.
- `try/except/finally`.
- Encadenamiento de excepciones.
- Archivo de logs.
- Datos almacenados en objetos y listas, sin base de datos.
- 12 operaciones automáticas de prueba en `main.py`.

## Interfaz gráfica

La aplicación gráfica incluye:

1. Panel principal.
2. Gestión de clientes.
3. Gestión de servicios.
4. Gestión de reservas.
5. Consulta de logs.
6. Ventanas de validación y mensajes de error.

## Ejecutar la aplicación gráfica

```bash
python main_gui.py
```

En Windows también puede utilizar:

```bash
py main_gui.py
```

## Ejecutar con datos de demostración

```bash
python demo_gui.py
```

Esto carga clientes, servicios y una reserva de ejemplo para facilitar la presentación.

## Ejecutar las 12 pruebas automáticas

```bash
python main.py
```

## Estructura

```text
software_fj_fase4_gui/
│
├── main.py
├── main_gui.py
├── demo_gui.py
├── datos.py
├── excepciones.py
├── logger_config.py
├── README.md
├── requirements.txt
├── modelos/
│   ├── __init__.py
│   ├── entidad.py
│   ├── cliente.py
│   ├── servicio.py
│   └── reserva.py
├── vistas/
│   ├── __init__.py
│   ├── ui_utils.py
│   ├── ventana_principal.py
│   ├── clientes_view.py
│   ├── servicios_view.py
│   ├── reservas_view.py
│   └── logs_view.py
└── logs/
```

## Importante

La interfaz gráfica no reemplaza las clases orientadas a objetos. Las ventanas consumen las mismas clases `Cliente`, `Servicio` y `Reserva`, por lo que las validaciones, excepciones y el polimorfismo siguen formando parte de la lógica principal del sistema.

No se utiliza ningún motor de base de datos.

## Autores

Agregar aquí los nombres de los cinco integrantes del grupo.

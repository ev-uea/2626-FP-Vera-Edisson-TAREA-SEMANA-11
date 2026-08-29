# Sistema de Gestión de Restaurante - Semana 11

**Estudiante:** Edisson Vera  
**Asignatura:** Programación Orientada a Objetos  
**Semana:** 11 -Fundamentos de colecciones aplicados a relaciones, ventas y persistencia JSON en restaurante_app
---

## 1. Descripción General del Proyecto
Esta versión mejora el sistema `restaurante_app` incorporando la entidad `Venta` para relacionar usuarios y productos en transacciones reales. Administra el control de inventario (`stock`), filtra las ventas por usuario mediante el recorrido de colecciones y extiende la persistencia JSON a tres entidades: **Productos**, **Usuarios** y **Ventas**.

---

## 2. Estructura Modular del Proyecto

```text
restaurante_app/
├── datos/
│   ├── productos.json       # Persistencia de productos y stock actualizado
│   ├── usuarios.json        # Persistencia de usuarios registrados
│   └── ventas.json          # Persistencia de las transacciones efectuadas
├── modelos/
│   ├── __init__.py
│   ├── producto.py          # Clase Producto con validación de stock
│   ├── usuario.py           # Clase Usuario
│   └── venta.py             # Clase Venta (Usuario ID + Producto Código + Cantidad)
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py  # Centralización I/O para las 3 colecciones JSON
│   └── restaurante.py       # Lógica del negocio, ventas y consultas
├── main.py                  # Interfaz de consola mediante funciones y mapeos
└── README.md
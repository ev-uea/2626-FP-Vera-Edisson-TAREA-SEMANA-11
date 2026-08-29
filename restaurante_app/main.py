import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from servicios.restaurante import Restaurante
from servicios.archivo_servicio import ArchivoServicio
from modelos.producto import Producto
from modelos.usuario import Usuario

# Tupla inmutable de opciones del menú
OPCIONES_MENU: tuple[str, ...] = (
    "========================================",
    "        SISTEMA DE RESTAURANTE",
    "========================================",
    "1. Registrar producto",
    "2. Buscar producto",
    "3. Actualizar producto",
    "4. Eliminar producto",
    "5. Listar productos",
    "----------------------------------------",
    "6. Registrar usuario",
    "7. Listar usuarios",
    "----------------------------------------",
    "8. Vender producto",
    "9. Consultar ventas por usuario",
    "10. Mostrar categorías de productos",
    "11. Salir",
    "========================================"
)

# Rutas de los archivos JSON
RUTA_PROD = os.path.join(BASE_DIR, "datos", "productos.json")
RUTA_USER = os.path.join(BASE_DIR, "datos", "usuarios.json")
RUTA_VENT = os.path.join(BASE_DIR, "datos", "ventas.json")

archivo_servicio = ArchivoServicio(RUTA_PROD, RUTA_USER, RUTA_VENT)
servicio_restaurante = Restaurante("Gourmet Express")

def sincronizar_productos() -> None:
    archivo_servicio.guardar_productos(servicio_restaurante.obtener_productos())

def sincronizar_usuarios() -> None:
    archivo_servicio.guardar_usuarios(servicio_restaurante.obtener_usuarios())

def sincronizar_ventas() -> None:
    archivo_servicio.guardar_ventas(servicio_restaurante.obtener_ventas())

# Funciones coordinadoras del menú
def ejecutar_registrar_producto() -> None:
    print("\n--- REGISTRAR PRODUCTO ---")
    codigo = input("Código: ").strip()
    nombre = input("Nombre: ").strip()
    categoria = input("Categoría: ").strip()
    try:
        precio = float(input("Precio: "))
        stock = int(input("Stock inicial: "))
        nuevo_p = Producto(codigo, nombre, categoria, precio, stock)
        if servicio_restaurante.registrar_producto(nuevo_p):
            sincronizar_productos()
            print(f"¡Éxito! Producto '{nombre}' registrado.")
    except ValueError as err:
        print(f"[Error de Entrada/Validación]: {err}")

def ejecutar_buscar_producto() -> None:
    print("\n--- BUSCAR PRODUCTO ---")
    codigo = input("Código a buscar: ").strip()
    prod = servicio_restaurante.buscar_producto_por_codigo(codigo)
    if prod:
        print("\n" + prod.mostrar_informacion())
    else:
        print(f"\n[Aviso]: No existe producto con código '{codigo}'.")

def ejecutar_actualizar_producto() -> None:
    print("\n--- ACTUALIZAR PRODUCTO ---")
    codigo = input("Código del producto a actualizar: ").strip()
    if not servicio_restaurante.buscar_producto_por_codigo(codigo):
        print(f"[Error]: Producto con código '{codigo}' no existe.")
        return
    nombre = input("Nuevo nombre: ").strip()
    categoria = input("Nueva categoría: ").strip()
    try:
        precio = float(input("Nuevo precio: "))
        stock = int(input("Nuevo stock: "))
        if servicio_restaurante.actualizar_producto(codigo, nombre, categoria, precio, stock):
            sincronizar_productos()
            print("¡Éxito! Producto actualizado.")
    except ValueError as err:
        print(f"[Error de Entrada/Validación]: {err}")

def ejecutar_eliminar_producto() -> None:
    print("\n--- ELIMINAR PRODUCTO ---")
    codigo = input("Código del producto a eliminar: ").strip()
    if servicio_restaurante.eliminar_producto(codigo):
        sincronizar_productos()
        print(f"¡Éxito! Producto con código '{codigo}' eliminado.")

def ejecutar_listar_productos() -> None:
    servicio_restaurante.listar_productos()

def ejecutar_registrar_usuario() -> None:
    print("\n--- REGISTRAR USUARIO ---")
    identificacion = input("Identificación/Cédula: ").strip()
    nombre = input("Nombre completo: ").strip()
    correo = input("Correo: ").strip()
    try:
        usr = Usuario(identificacion, nombre, correo)
        if servicio_restaurante.registrar_usuario(usr):
            sincronizar_usuarios()
            print(f"¡Éxito! Usuario '{nombre}' registrado.")
    except ValueError as err:
        print(f"[Error de Entrada/Validación]: {err}")

def ejecutar_listar_usuarios() -> None:
    servicio_restaurante.listar_usuarios()

def ejecutar_vender_producto() -> None:
    print("\n--- REALIZAR VENTA ---")
    id_usuario = input("Identificación del usuario comprador: ").strip()
    cod_producto = input("Código del producto a comprar: ").strip()
    try:
        cantidad = int(input("Cantidad a comprar: "))
        if servicio_restaurante.vender_producto(cod_producto, id_usuario, cantidad):
            sincronizar_productos()
            sincronizar_ventas()
            print(f"\n¡Venta registrada con éxito! Se descontaron {cantidad} unidades del stock.")
    except ValueError as err:
        print(f"[Error de Entrada/Validación]: {err}")

def ejecutar_consultar_ventas_usuario() -> None:
    print("\n--- CONSULTAR VENTAS POR USUARIO ---")
    id_usuario = input("Identificación del usuario: ").strip()
    usr = servicio_restaurante.buscar_usuario_por_id(id_usuario)
    if not usr:
        print(f"[Error]: No se encontró ningún usuario registrado con ID '{id_usuario}'.")
        return

    ventas = servicio_restaurante.consultar_ventas_por_usuario(id_usuario)
    print(f"\nHistorial de ventas asociadas a: {usr.nombre} (ID: {usr.identificacion})")
    print("-------------------------------------------------------------------------")
    if not ventas:
        print("El usuario no registra compras realizadas.")
        return

    for v in ventas:
        prod = servicio_restaurante.buscar_producto_por_codigo(v.producto_codigo)
        nombre_prod = prod.nombre if prod else "Producto descontinuado/no encontrado"
        print(f"• Producto: {nombre_prod} (Código: {v.producto_codigo}) | Unidades: {v.cantidad}")
    print("-------------------------------------------------------------------------")

def ejecutar_mostrar_categorias() -> None:
    print("\n--- CATEGORÍAS ÚNICAS ---")
    cats = servicio_restaurante.obtener_categorias_unicas()
    if not cats:
        print("No hay categorías disponibles.")
        return
    for c in cats:
        print(f"• {c}")

def ejecutar_salir() -> None:
    print("\n¡Gracias por usar el Sistema de Restaurante!")

def main() -> None:
    # Carga de la trinidad de datos JSON
    prods = archivo_servicio.cargar_productos()
    usrs = archivo_servicio.cargar_usuarios()
    vents = archivo_servicio.cargar_ventas()
    servicio_restaurante.cargar_datos_iniciales(prods, usrs, vents)

    mapa_acciones = {
        "1": ejecutar_registrar_producto,
        "2": ejecutar_buscar_producto,
        "3": ejecutar_actualizar_producto,
        "4": ejecutar_eliminar_producto,
        "5": ejecutar_listar_productos,
        "6": ejecutar_registrar_usuario,
        "7": ejecutar_listar_usuarios,
        "8": ejecutar_vender_producto,
        "9": ejecutar_consultar_ventas_usuario,
        "10": ejecutar_mostrar_categorias,
        "11": ejecutar_salir
    }

    while True:
        print()
        for linea in OPCIONES_MENU:
            print(linea)
        opcion = input("Seleccione una opción (1-11): ").strip()

        accion = mapa_acciones.get(opcion)
        if accion:
            accion()
            if opcion == "11":
                break
        else:
            print("\n[Error]: Opción no válida. Ingrese un número de 1 a 11.")

if __name__ == "__main__":
    main()
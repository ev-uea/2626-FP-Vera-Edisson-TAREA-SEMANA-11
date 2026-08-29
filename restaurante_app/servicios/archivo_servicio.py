import json
import os
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

class ArchivoServicio:
    """Servicio encargado centralizadamente de la lectura y escritura JSON de Productos, Usuarios y Ventas."""

    def __init__(self, ruta_productos: str, ruta_usuarios: str, ruta_ventas: str) -> None:
        self.ruta_productos: str = ruta_productos
        self.ruta_usuarios: str = ruta_usuarios
        self.ruta_ventas: str = ruta_ventas
        self._asegurar_directorios()

    def _asegurar_directorios(self) -> None:
        """Crea la carpeta contenedora de los datos si no existe."""
        for ruta in [self.ruta_productos, self.ruta_usuarios, self.ruta_ventas]:
            directorio = os.path.dirname(ruta)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio, exist_ok=True)

    # ------------------ PERSISTENCIA PRODUCTOS ------------------
    def guardar_productos(self, lista_productos: list[Producto]) -> bool:
        try:
            datos = [prod.a_diccionario() for prod in lista_productos]
            with open(self.ruta_productos, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        except PermissionError:
            print(f"\n[Error Permiso]: No hay permisos para escribir en '{self.ruta_productos}'.")
            return False

    def cargar_productos(self) -> list[Producto]:
        productos: list[Producto] = []
        try:
            with open(self.ruta_productos, "r", encoding="utf-8") as archivo:
                contenido = json.load(archivo)
                for reg in contenido:
                    if isinstance(reg, dict):
                        productos.append(Producto.desde_diccionario(reg))
        except FileNotFoundError:
            print(f"[Info]: Archivo '{self.ruta_productos}' no encontrado. Se iniciará catálogo vacío.")
        except json.JSONDecodeError:
            print(f"[Error]: Formato JSON inválido en '{self.ruta_productos}'.")
        except PermissionError:
            print(f"[Error Permiso]: Sin permisos de lectura para '{self.ruta_productos}'.")
        except (KeyError, ValueError) as err:
            print(f"[Error Datos]: Registro de producto omitido por datos inválidos: {err}")
        return productos

    # ------------------ PERSISTENCIA USUARIOS ------------------
    def guardar_usuarios(self, lista_usuarios: list[Usuario]) -> bool:
        try:
            datos = [usr.a_diccionario() for usr in lista_usuarios]
            with open(self.ruta_usuarios, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        except PermissionError:
            print(f"\n[Error Permiso]: No hay permisos para escribir en '{self.ruta_usuarios}'.")
            return False

    def cargar_usuarios(self) -> list[Usuario]:
        usuarios: list[Usuario] = []
        try:
            with open(self.ruta_usuarios, "r", encoding="utf-8") as archivo:
                contenido = json.load(archivo)
                for reg in contenido:
                    if isinstance(reg, dict):
                        usuarios.append(Usuario.desde_diccionario(reg))
        except FileNotFoundError:
            print(f"[Info]: Archivo '{self.ruta_usuarios}' no encontrado. Se iniciará lista vacía.")
        except json.JSONDecodeError:
            print(f"[Error]: Formato JSON inválido en '{self.ruta_usuarios}'.")
        except PermissionError:
            print(f"[Error Permiso]: Sin permisos de lectura para '{self.ruta_usuarios}'.")
        except (KeyError, ValueError) as err:
            print(f"[Error Datos]: Registro de usuario omitido por datos inválidos: {err}")
        return usuarios

    # ------------------ PERSISTENCIA VENTAS ------------------
    def guardar_ventas(self, lista_ventas: list[Venta]) -> bool:
        try:
            datos = [v.a_diccionario() for v in lista_ventas]
            with open(self.ruta_ventas, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        except PermissionError:
            print(f"\n[Error Permiso]: No hay permisos para escribir en '{self.ruta_ventas}'.")
            return False

    def cargar_ventas(self) -> list[Venta]:
        ventas: list[Venta] = []
        try:
            with open(self.ruta_ventas, "r", encoding="utf-8") as archivo:
                contenido = json.load(archivo)
                for reg in contenido:
                    if isinstance(reg, dict):
                        ventas.append(Venta.desde_diccionario(reg))
        except FileNotFoundError:
            print(f"[Info]: Archivo '{self.ruta_ventas}' no encontrado. Se iniciará lista de ventas vacía.")
        except json.JSONDecodeError:
            print(f"[Error]: Formato JSON inválido en '{self.ruta_ventas}'.")
        except PermissionError:
            print(f"[Error Permiso]: Sin permisos de lectura para '{self.ruta_ventas}'.")
        except (KeyError, ValueError) as err:
            print(f"[Error Datos]: Registro de venta omitido por datos inválidos: {err}")
        return ventas
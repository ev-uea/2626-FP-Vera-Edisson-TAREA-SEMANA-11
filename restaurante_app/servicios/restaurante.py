from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

class Restaurante:
    """Servicio de negocio que administra colecciones de productos, usuarios y ventas."""

    def __init__(self, nombre_establecimiento: str) -> None:
        self.nombre_establecimiento: str = nombre_establecimiento
        self._productos: list[Producto] = []
        self._usuarios: list[Usuario] = []
        self._ventas: list[Venta] = []

    # Getters y Cargas de colecciones
    def obtener_productos(self) -> list[Producto]:
        return self._productos

    def obtener_usuarios(self) -> list[Usuario]:
        return self._usuarios

    def obtener_ventas(self) -> list[Venta]:
        return self._ventas

    def cargar_datos_iniciales(self, productos: list[Producto], usuarios: list[Usuario], ventas: list[Venta]) -> None:
        self._productos = productos
        self._usuarios = usuarios
        self._ventas = ventas

    # Operaciones Productos
    def registrar_producto(self, producto: Producto) -> bool:
        if self.buscar_producto_por_codigo(producto.codigo) is not None:
            print(f"\n[Error]: El código '{producto.codigo}' ya pertenece a un producto.")
            return False
        self._productos.append(producto)
        return True

    def buscar_producto_por_codigo(self, codigo: str) -> Producto | None:
        for p in self._productos:
            if p.codigo.lower() == codigo.strip().lower():
                return p
        return None

    def actualizar_producto(self, codigo: str, nuevo_nombre: str, nueva_categoria: str, nuevo_precio: float, nuevo_stock: int) -> bool:
        producto = self.buscar_producto_por_codigo(codigo)
        if producto is None:
            print(f"\n[Error]: No existe producto con código '{codigo}'.")
            return False
        temp = Producto(codigo, nuevo_nombre, nueva_categoria, nuevo_precio, nuevo_stock)
        producto.nombre = temp.nombre
        producto.categoria = temp.categoria
        producto.precio = temp.precio
        producto.stock = temp.stock
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        producto = self.buscar_producto_por_codigo(codigo)
        if producto is None:
            print(f"\n[Error]: No existe producto con código '{codigo}'.")
            return False
        self._productos.remove(producto)
        return True

    def listar_productos(self) -> None:
        print(f"\n================ CATÁLOGO DE PRODUCTOS: {self.nombre_establecimiento.upper()} ================")
        if not self._productos:
            print("No hay productos en el sistema.")
            return
        for p in self._productos:
            print(p.mostrar_informacion())
        print("=========================================================================")

    def obtener_categorias_unicas(self) -> set[str]:
        return {p.categoria for p in self._productos}

    # Operaciones Usuarios
    def registrar_usuario(self, usuario: Usuario) -> bool:
        if self.buscar_usuario_por_id(usuario.identificacion) is not None:
            print(f"\n[Error]: El usuario con ID '{usuario.identificacion}' ya está registrado.")
            return False
        self._usuarios.append(usuario)
        return True

    def buscar_usuario_por_id(self, identificacion: str) -> Usuario | None:
        for u in self._usuarios:
            if u.identificacion == identificacion.strip():
                return u
        return None

    def listar_usuarios(self) -> None:
        print("\n================ LISTADO DE USUARIOS ================")
        if not self._usuarios:
            print("No hay usuarios registrados.")
            return
        for u in self._usuarios:
            print(u.mostrar_informacion())
        print("=====================================================")

    # Operaciones Ventas (Relación Usuario + Producto)
    def vender_producto(self, codigo_producto: str, identificacion_usuario: str, cantidad: int) -> bool:
        """Registra la venta relacionando usuario y producto, descontando stock solo si las validaciones pasan."""
        usuario = self.buscar_usuario_por_id(identificacion_usuario)
        producto = self.buscar_producto_por_codigo(codigo_producto)

        if usuario is None:
            print(f"\n[Error Venta]: El usuario con ID '{identificacion_usuario}' no existe.")
            return False
        if producto is None:
            print(f"\n[Error Venta]: El producto con código '{codigo_producto}' no existe.")
            return False
        if cantidad <= 0:
            print("\n[Error Venta]: La cantidad a comprar debe ser mayor a cero.")
            return False
        if producto.stock < cantidad:
            print(f"\n[Error Venta]: Stock insuficiente. Disponible: {producto.stock}, Solicitado: {cantidad}.")
            return False

        # Realizar la transacción
        producto.vender(cantidad)
        venta = Venta(usuario.identificacion, producto.codigo, cantidad)
        self._ventas.append(venta)
        return True

    def consultar_ventas_por_usuario(self, identificacion_usuario: str) -> list[Venta]:
        """Filtra y retorna todas las ventas asociadas a la identificación de un usuario."""
        ventas_usuario: list[Venta] = []
        for venta in self._ventas:
            if venta.usuario_id == identificacion_usuario.strip():
                ventas_usuario.append(venta)
        return ventas_usuario
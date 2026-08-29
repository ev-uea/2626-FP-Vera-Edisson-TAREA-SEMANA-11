class Producto:
    """Entidad que representa un producto del restaurante con stock."""

    def __init__(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int = 0) -> None:
        if precio <= 0:
            raise ValueError("El precio debe ser mayor a cero.")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        if not codigo.strip() or not nombre.strip() or not categoria.strip():
            raise ValueError("Código, nombre y categoría no pueden estar vacíos.")

        self.codigo: str = codigo.strip()
        self.nombre: str = nombre.strip()
        self.categoria: str = categoria.strip()
        self.precio: float = float(precio)
        self.stock: int = int(stock)

    def vender(self, cantidad: int) -> None:
        """Disminuye el stock del producto tras validar la cantidad."""
        if cantidad <= 0:
            raise ValueError("La cantidad a vender debe ser mayor a cero.")
        if cantidad > self.stock:
            raise ValueError("Stock insuficiente para realizar la venta.")
        self.stock -= cantidad

    def mostrar_informacion(self) -> str:
        """Devuelve representación formateada del producto."""
        return f"[PRODUCTO] Código: {self.codigo} | Nombre: {self.nombre} | Categoría: {self.categoria} | Precio: ${self.precio:.2f} | Stock: {self.stock}"

    def a_diccionario(self) -> dict:
        """Serializa el objeto Producto a un diccionario para JSON."""
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock
        }

    @staticmethod
    def desde_diccionario(datos: dict) -> "Producto":
        """Reconstruye una instancia de Producto desde un diccionario JSON."""
        try:
            return Producto(
                codigo=str(datos["codigo"]),
                nombre=str(datos["nombre"]),
                categoria=str(datos["categoria"]),
                precio=float(datos["precio"]),
                stock=int(datos.get("stock", 0))
            )
        except KeyError as e:
            raise KeyError(f"Clave faltante en datos de Producto: {e}")
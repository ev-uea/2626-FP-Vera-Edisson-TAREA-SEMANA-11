class Venta:
    """Entidad que representa la relación y transacción de compra entre un Usuario y un Producto."""

    def __init__(self, usuario_id: str, producto_codigo: str, cantidad: int) -> None:
        if not usuario_id.strip() or not producto_codigo.strip():
            raise ValueError("La venta requiere la identificación del usuario y el código del producto.")
        if cantidad <= 0:
            raise ValueError("La cantidad vendida debe ser mayor a cero.")

        self.usuario_id: str = usuario_id.strip()
        self.producto_codigo: str = producto_codigo.strip()
        self.cantidad: int = int(cantidad)

    def mostrar_informacion(self) -> str:
        """Devuelve la información formateada de la venta."""
        return f"[VENTA] Usuario ID: {self.usuario_id} | Producto Código: {self.producto_codigo} | Cantidad: {self.cantidad}"

    def a_diccionario(self) -> dict:
        """Serializa la Venta a un diccionario para JSON."""
        return {
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "cantidad": self.cantidad
        }

    @staticmethod
    def desde_diccionario(datos: dict) -> "Venta":
        """Reconstruye una instancia de Venta desde un diccionario JSON."""
        try:
            return Venta(
                usuario_id=str(datos["usuario_id"]),
                producto_codigo=str(datos["producto_codigo"]),
                cantidad=int(datos["cantidad"])
            )
        except KeyError as e:
            raise KeyError(f"Clave faltante en datos de Venta: {e}")
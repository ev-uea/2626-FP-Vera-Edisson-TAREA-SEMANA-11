class Usuario:
    """Entidad que representa a un usuario registrado en el sistema."""

    def __init__(self, identificacion: str, nombre: str, correo: str) -> None:
        if not identificacion.strip() or not nombre.strip() or not correo.strip():
            raise ValueError("Identificación, nombre y correo son obligatorios.")

        self.identificacion: str = identificacion.strip()
        self.nombre: str = nombre.strip()
        self.correo: str = correo.strip()

    def mostrar_informacion(self) -> str:
        """Devuelve detalles del usuario."""
        return f"[USUARIO] ID: {self.identificacion} | Nombre: {self.nombre} | Correo: {self.correo}"

    def a_diccionario(self) -> dict:
        """Serializa el objeto Usuario a un diccionario para JSON."""
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo
        }

    @staticmethod
    def desde_diccionario(datos: dict) -> "Usuario":
        """Reconstruye una instancia de Usuario desde un diccionario JSON."""
        try:
            return Usuario(
                identificacion=str(datos["identificacion"]),
                nombre=str(datos["nombre"]),
                correo=str(datos["correo"])
            )
        except KeyError as e:
            raise KeyError(f"Clave faltante en datos de Usuario: {e}")
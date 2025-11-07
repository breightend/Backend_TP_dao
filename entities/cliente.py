from entities.persona import Persona


class Cliente(Persona):
    def __init__(
        self,
        nombre: str,
        apellido: str,
        fechaNacimiento: str,
        dni: str,
        telefono: str,
        email: str,
    ):
        super().__init__(nombre, apellido, fechaNacimiento, dni, telefono, email)

    def mostrar_informacion(self):
        return super().mostrar_informacion()

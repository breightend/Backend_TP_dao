from entities.persoja import Persona


class Empleado(Persona):
    def __init__(
        self,
        nombre: str,
        apellido: str,
        fechaNacimiento: str,
        dni: str,
        telefono: str,
        email: str,
        legajo: str,
        puesto: str,
    ):
        super().__init__(nombre, apellido, fechaNacimiento, dni, telefono, email)
        self.legajo = legajo
        self.puesto = puesto

    def get_description(self) -> str:
        return (
            f"Empleado ID: {self.legajo}, Nombre: {self.nombre} {self.apellido}, "
            f"Puesto: {self.puesto}, Salario: {self.salario}"
        )

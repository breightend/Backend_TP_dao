from abc import ABC, abstractmethod


class Persona(ABC):
    def __init__(self, nombre: str, apellido: str, fechaNacimiento: str, dni: str, telefono: str, email: str):
        self.nombre = nombre
        self.apellido = apellido
        self.fechaNacimiento = fechaNacimiento
        self.dni = dni
        self.telefono = telefono
        self.email = email


    @abstractmethod
    def get_description(self) -> str:
        pass

    
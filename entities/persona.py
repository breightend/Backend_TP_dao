from abc import ABC, ABCMeta 
from sqlalchemy import Column, DateTime, Integer, String
from db.base import Base

Declarative_meta = type(Base)

class CombinedMeta(ABCMeta, Declarative_meta): 
    pass

class Persona(Base, ABC, metaclass=CombinedMeta):

    __abstract__ = True

    dni = Column("dni", Integer, primary_key=True, autoincrement=False)
    direccion = Column("direccion", String(200), nullable=False)
    nombre = Column("nombre", String(100), nullable=False)
    apellido = Column("apellido", String(100), nullable=False)
    email = Column("email", String(100), nullable=False)
    telefono = Column("telefono", String(20), nullable=False)
    fechaNacimiento = Column("fecha_nacimiento", String(10), nullable=False)

    def __init__(
        self,
        nombre: str,
        apellido: str,
        direccion: str,
        fechaNacimiento: str,
        dni: int,
        telefono: int,
        email: str,
    ):
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.fechaNacimiento = fechaNacimiento
        self.dni = dni
        self.telefono = telefono
        self.email = email

    def mostrar_informacion(self) -> str:
        return (
            f"Nombre: {self.nombre}, Apellido: {self.apellido}, "
            f"Fecha de Nacimiento: {self.fechaNacimiento}, DNI: {self.dni}, "
            f"Teléfono: {self.telefono}, Email: {self.email}"
        )

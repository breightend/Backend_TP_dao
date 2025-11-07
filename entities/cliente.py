from entities.persona import Persona
from db.definitions import clientes
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Cliente(Persona, Base):
  
    __table__ = clientes
  
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

    def persist(self):
      try:
        
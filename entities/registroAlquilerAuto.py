from db.connection import DatabaseEngineSingleton
from db.base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, sessionmaker

from typing import List
from .cliente import Cliente
from .empleado import Empleado
from .auto import Auto
from datetime import datetime


class RegistroAlquilerAuto(Base):
  __tablename__ = "Alquileres_de_auto"

  id = Column("id_alquiler", Integer, primary_key=True)
  patente_vehiculo = Column("patente_vehiculo", String, ForeignKey("Automoviles.patente"))
  fechaInicio = Column("fecha_inicio", String)
  fechaFin = Column("fecha_fin", String)
  precio = Column("precio", Float)
  dni_cliente = Column("dni_cliente", Integer, ForeignKey("Clientes.dni"))
  legajo_empleado = Column("legajo_empleado", Integer, ForeignKey("Empleados.legajo"))

  auto = relationship(Auto)
  cliente = relationship(Cliente)
  empleado = relationship(Empleado)
  
  def __init__(self, fechaInicio: str, precio: float, dni_cliente: int, legajo_empleado: int, patente_vehiculo: str) -> None:
    self.fechaInicio = fechaInicio
    self.fechaFin = ""
    self.precio = precio
    self.dni_cliente = dni_cliente
    self.legajo_empleado = legajo_empleado
    self.patente_vehiculo = patente_vehiculo
    self.sanciones = []
  
  def finalizarAlquiler(self):
    self.fechaInicio = datetime.now().strftime("%Y-%m-%d")
  
  def calcularCostoTotal(self):
    pass
    
  def calcularCostoSanciones(self):
    pass

  def obtenerSancionesDeAlquiler(self):
    from .sancion import Sancion
    from sqlalchemy.orm import joinedload

    engine = DatabaseEngineSingleton().engine
    Session = sessionmaker(bind=engine)
    session = Session()

    sanciones = (
        session.query(Sancion)
        .options(joinedload(Sancion.tipo_sancion), joinedload(Sancion.estado))
        .filter(Sancion.id_alquiler == self.id)
        .all()
    )
    session.close()
    
    return sanciones
  
  def obtenerSancionesDict(self):

    sanciones = self.obtenerSancionesDeAlquiler()

    return [sancion.to_dict() for sancion in sanciones]

  def persist(self):
    engine = DatabaseEngineSingleton().engine
    Session = sessionmaker(bind=engine)
    session = Session()

    session.add(self)
    try:
      session.commit()
    except Exception as e:
      session.rollback()
      raise e
    finally:
      session.close()

  @classmethod
  def get_all_rentals(cls):
    engine = DatabaseEngineSingleton().engine
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
      rentals = session.query(cls).all()
    except Exception as e:
      session.rollback()
      raise e
    finally:
      session.close()

    return rentals

  @classmethod
  def get_all_rentals_description(cls):
    engine = DatabaseEngineSingleton().engine
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
      rentals = session.query(cls).all()
      return [rental.to_dict() for rental in rentals]
    except Exception as e:
      session.rollback()
      raise e
    finally:
      session.close()

  def to_dict(self):
    return {
      "id": self.id,
      "vehiculo": self.auto.to_dict() if self.auto else None,
      "fechaInicio": self.fechaInicio,
      "fechaFin": self.fechaFin,
      "precio": self.precio,
      "cliente": self.cliente.to_dict() if self.cliente else None,
      "empleado": self.empleado.to_dict() if self.empleado else None,
      "sanciones": self.obtenerSancionesDict()
    }

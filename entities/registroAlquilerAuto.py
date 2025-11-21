from db.connection import DatabaseEngineSingleton
from db.base import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, sessionmaker

from typing import List
from cliente import Cliente
from empleado import Empleado
from auto import Auto
from sancion import Sancion


class RegistroAlquilerAuto(Base):


  __tablename__ = "Alquileres_de_autos"

  id = Column("id_alquiler", Integer, primary_key=True)
  patente_vehiculo = Column("patente_vehiculo", Integer, ForeignKey("Autos.id"))
  fechaInicio = Column("fecha_inicio", String)
  fechaFin = Column("fecha_fin", String)
  precio = Column("precio", Float)
  dni_cliente = Column("dni_cliente", Integer, ForeignKey("Clientes.dni"))
  legajo_empleado = Column("legajo_empleado", Integer, ForeignKey("Empleados.legajo"))
  sanciones: List[Sancion]

  auto = relationship("Auto", back_populates="alquileres")
  cliente = relationship("Cliente", back_populates="alquileres")
  empleado = relationship("Empleado", back_populates="alquileres")
  
  def __init__(self, fechaInicio: string, precio: float, dni_cliente: int, legajo_empleado: int, patente_vehiculo: string) -> None:
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
    if self.sanciones == []:
      engine = DatabaseEngineSingleton().engine
      Session = sessionmaker(bind=engine)
      session = Session()

      sanciones = session.query(Sancion).filter(Sancion.id_alquiler == self.id).all()
      session.close()
      self.sanciones = sanciones
    
    return self.sanciones

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

from db.connection import DatabaseEngineSingleton
from db.base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, sessionmaker

from typing import List
from .cliente import Cliente
from .empleado import Empleado
from .auto import Auto
from .estado import Estado
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
  id_estado = Column("id_estado", Integer, ForeignKey("Estados.id_estado"))

  auto = relationship(Auto)
  cliente = relationship(Cliente)
  empleado = relationship(Empleado)
  estado = relationship(Estado)

  def __init__(self, fechaInicio: str, precio: float, dni_cliente: int, legajo_empleado: int, patente_vehiculo: str, fechaFin: str, id_estado: int) -> None:
    self.fechaInicio = fechaInicio
    self.fechaFin = fechaFin 
    self.precio = precio
    self.dni_cliente = dni_cliente
    self.legajo_empleado = legajo_empleado
    self.patente_vehiculo = patente_vehiculo
    self.id_estado = id_estado
    self.sanciones = []
  
  def finalizarAlquiler(self):
    estadosDeAlquiler = Estado.get_all_estados_de_ambito("Alquiler")
    for estado in estadosDeAlquiler:
      if estado["nombre"] == "Finalizado":
        self.id_estado = estado["id_estado"]
        break

  def actualizar_alquiler(self, nueva_fecha_fin: str, costo_diario: float):
      from datetime import timedelta
      fmt = "%Y-%m-%d"
      d1 = datetime.strptime(self.fechaFin.strip(), fmt).date()
      d1 = d1 - timedelta(days=1)
      d2 = datetime.strptime(nueva_fecha_fin.strip(), fmt).date()
      
      dias_extra = (d2 - d1).days
      
      print(f"DEBUG: Extender alquiler. Fecha actual (ajustada): {d1}, Nueva fecha: {d2}, Dias extra: {dias_extra}, Costo diario: {costo_diario}")
      
      if dias_extra > 0:
          self.precio += dias_extra * costo_diario
          self.fechaFin = (d2 + timedelta(days=1)).strftime(fmt)
  
  def calcularCostoTotal(self):
    return self.precio + self.calcularCostoSanciones()
    
  def calcularCostoSanciones(self):
    return sum(sancion.costo for sancion in self.sanciones)

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

  @classmethod
  def get_rental_by_id(cls, id: int, objectNeeded: bool):
    engine = DatabaseEngineSingleton().engine
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
      rental = session.query(cls).filter(cls.id == id).first()
      if objectNeeded:
        return rental
      rental_dict = rental.to_dict()
      return rental_dict

    except Exception as e:
      session.rollback()
      raise e
    finally:
      session.close()

  @classmethod
  def get_active_rentals(cls):
    engine = DatabaseEngineSingleton().engine
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
      rentals = session.query(cls).filter(cls.id_estado != 9).all()
      return [rental.to_dict() for rental in rentals]
    except Exception as e:
      session.rollback()
      raise e
    finally:
      session.close()

  @classmethod
  def car_available(cls, patente_vehiculo: str, fecha_inicio: str, fecha_fin: str):
    engine = DatabaseEngineSingleton().engine
    Session = sessionmaker(bind=engine)
    session = Session()

    fmt = "%Y-%m-%d"
    d1 = datetime.strptime(fecha_inicio.strip(), fmt).date()
    d2 = datetime.strptime(fecha_fin.strip(), fmt).date()

    try:
      rentals = session.query(cls).filter(cls.patente_vehiculo == patente_vehiculo).filter(cls.id_estado != 9).all()
      if rentals == []:
        return True
      for rental in rentals:
        rental_d1 = datetime.strptime(rental.fechaInicio.strip(), fmt).date()
        rental_d2 = datetime.strptime(rental.fechaFin.strip(), fmt).date()

        if d1 < rental_d2 and d2 > rental_d1:
          return False
      return True
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

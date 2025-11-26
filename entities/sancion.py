from .tipoSancion import TipoSancion
from .daño import Daño

from db.connection import DatabaseEngineSingleton
from db.base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, sessionmaker, joinedload

class Sancion(Base):
    __tablename__ = "Sanciones"
    
    id = Column("id_sancion", Integer, primary_key=True)
    fecha = Column("fecha", String(10), nullable=False)
    id_tipo_sancion = Column("id_tipo_sancion", Integer, ForeignKey("Tipo_Sancion.id_sancion"))
    id_estado = Column("id_estado", Integer, ForeignKey("Estados.id_estado"))
    costo_base = Column("costo_base", Float, nullable=False)
    descripcion = Column("descripcion", String(200), nullable=False)
    id_alquiler = Column("id_alquiler", Integer, ForeignKey("Alquileres_de_auto.id_alquiler"))

    tipo_sancion = relationship("TipoSancion")
    estado = relationship("Estado")
    
    
    def __init__(self, fecha: str, id_tipo_sancion: int, id_estado: int, costo_base: float, descripcion: str, id_alquiler: int):
        self.fecha = fecha
        self.id_tipo_sancion = id_tipo_sancion
        self.id_estado = id_estado
        self.costo_base = costo_base
        self.descripcion = descripcion
        self.id_alquiler = id_alquiler
    
    def calcularCostoTotal(self) -> float:
        
        daños = self.obtenerDaños()

        if daños == []:
            return self.costo_base
        costoTotalDaños = sum(daño.calcularCostoTotal() for daño in daños)
        return costoTotalDaños + self.costo_base

    def tiempoDeSancion(self) -> int:
        return self.tipo.getAños()
    
    def persist(self):
        engine = DatabaseEngineSingleton().engine
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(self)
        try:
            session.commit()
            return self.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def obtenerDaños(self):
        engine = DatabaseEngineSingleton().engine
        Session = sessionmaker(bind=engine)
        session = Session()

        daños = session.query(Daño).options(joinedload(Daño.tipo_daño)).filter(Daño.sancion_id == self.id).all()
        session.close()
        
        return daños

    
    @classmethod
    def get_all_sanciones_of_alquiler(cls, alquiler_id: int):
        engine = DatabaseEngineSingleton().engine
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            sanciones = session.query(Sancion).filter(Sancion.id_alquiler == alquiler_id).all()
            sanciones = [s.to_dict() for s in sanciones]
            return sanciones
        except Exception as e:
            print(f"Error occurred while retrieving Sanciones: {e}")
            return []
        finally:
            session.close()

    @classmethod
    def get_sancion_by_id(cls, id: int):
        engine = DatabaseEngineSingleton().engine
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            sancion = session.query(Sancion).filter(Sancion.id == id).first()
            return sancion
        except Exception as e:
            print(f"Error occurred while retrieving Sancion: {e}")
            return None
        finally:
            session.close()

    @classmethod
    def get_all_estados_sanciones(cls):
        from .estado import Estado
        try:
            estados = Estado.get_all_estados_de_ambito("Sanciones")
            print(estados)
            return estados
        except Exception as e:
            print(f"Error occurred while retrieving Estados de Sanciones: {e}")
            return []

    @classmethod
    def get_sanciones_by_estado(cls, id_estado: int):
        engine = DatabaseEngineSingleton().engine
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            sanciones = session.query(Sancion).filter(Sancion.id_estado == id_estado).all()
            sanciones = [s.to_dict() for s in sanciones]
            return sanciones
        except Exception as e:
            print(f"Error occurred while retrieving Sanciones by estado: {e}")
            return []
        finally:
            session.close()



    def to_dict(self):
        return {
            "id_sancion": self.id,
            "fecha": self.fecha,
            "tipo_sancion": self.tipo_sancion.to_dict(),
            "estado": self.estado.to_dict(),
            "descripcion": self.descripcion,
            "id_alquiler": self.id_alquiler,
            "costo_total": self.calcularCostoTotal()
        }

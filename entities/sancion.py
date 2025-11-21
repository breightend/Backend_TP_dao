from tipoSancion import TipoSancion
from daño import Daño

from db.connection import DatabaseEngineSingleton
from db.base import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, sessionmaker

class Sancion(Base):
    __tablename__ = "Sanciones"
    
    id = Column("id_sancion", Integer, primary_key=True)
    fecha = Column("fecha", String(10), nullable=False)
    id_tipo_sancion = Column("id_tipo_sancion", Integer, ForeignKey("Tipo_Sancion.id_sancion"))
    id_estado = Column("id_estado", Integer, ForeignKey("Estados.id_estado"))
    costo_base = Column("costo_base", Float, nullable=False)
    descripcion = Column("descripcion", String(200), nullable=False)
    id_alquiler = Column("id_alquiler", Integer, ForeignKey("Alquileres_de_auto.id_alquiler"))
    
    daños: List[Daño]

    tipo_sancion = relationship("TipoSancion", back_populates="sanciones")
    estado = relationship("Estado", back_populates="sanciones")
    
    
    def __init__(self, fecha: str, tipo: TipoSancion, estado: Estado, costoBase: float, descripcion: str):
        self.fecha = fecha
        self.tipo = tipo
        self.estado = estado
        self.costoBase = costoBase
        self.descripcion = descripcion
        self.daños = []
    
    def calcularCostoTotal(self) -> float:
        costoTotalDaños = sum(daño.calcularCostoTotal() for daño in self.daños)
        return costoTotalDaños

    def tiempoDeSancion(self) -> int:
        return self.tipo.getAños()
    
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

    def obtenerDaños(self):
        if self.daños == []:
            engine = DatabaseEngineSingleton().engine
            Session = sessionmaker(bind=engine)
            session = Session()

            daños = session.query(Daño).filter(Daño.id_sancion == self.id).all()
            session.close()
            self.daños = daños
        
        return self.daños

    
    @classmethod
    def get_all_sanciones_of_alquiler(cls, alquiler_id: int):
        engine = DatabaseEngineSingleton().engine
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            sanciones = session.query(Sancion).filter(Sancion.id_alquiler == alquiler_id).all()
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


   

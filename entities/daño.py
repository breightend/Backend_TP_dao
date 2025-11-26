from .estado import Estado
from .tipoDaño import TipoDaño
from db.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from db.connection import DatabaseEngineSingleton

class Daño(Base):
    __tablename__ = "Daños"
    
    id = Column("id_daño", Integer, primary_key=True)
    fecha = Column("fecha", String(10), nullable=False)
    gravedad = Column("gravedad", Integer, nullable=False)
    estado_id = Column("id_estado", Integer, ForeignKey("Estados.id_estado"))
    tipo_daño_id = Column("id_tipo_daño", Integer, ForeignKey("Tipo_de_daño.id_daño"))
    sancion_id = Column("id_sancion", Integer, ForeignKey("Sanciones.id_sancion"))

    estado = relationship("Estado")
    tipo_daño = relationship("TipoDaño")
    sancion = relationship("Sancion")
    
    def __init__(self, fecha: str, gravedad: int, id_estado: int, id_tipo_daño: int, id_sancion: int):
        self.fecha = fecha
        self.estado_id = id_estado
        self.tipo_daño_id = id_tipo_daño
        self.sancion_id = id_sancion

        if gravedad < 1:
            self.gravedad = 1
        elif gravedad > 5:
            self.gravedad = 5
        else:
            self.gravedad = gravedad

    def getFecha(self) -> str:
        return self.fecha

    def getGravedad(self) -> int:
        return self.gravedad

    def getEstado(self) -> Estado:
        return self.estado

    def getTipoDaño(self) -> TipoDaño:
        return self.tipo_daño

    def calcularCostoTotal(self) -> float:
        if self.tipo_daño is None:
            return 0.0
        return int(self.tipo_daño.getCostoBase() * (1 + self.gravedad / 10))

    def actualizarEstado(self, nuevoEstado: Estado):
        self.estado = nuevoEstado

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

    def to_dict(self):
        return {
            "id_daño": self.id,
            "fecha": self.fecha,
            "gravedad": self.gravedad,
            "estado": self.estado.to_dict() if self.estado else None,
            "tipoDaño": self.tipo_daño.to_dict() if self.tipo_daño else None,
            "sancion": self.sancion.to_dict() if self.sancion else None
        }
    
    @classmethod
    def get_daño_by_id(cls, id: int):
        engine = DatabaseEngineSingleton().engine
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            daño = session.query(Daño).filter(Daño.id == id).first()
            return daño
        except Exception as e:
            print(f"Error occurred while retrieving Daño: {e}")
            return None
        finally:
            session.close()
    
    @classmethod
    def get_all_daños(cls):
        engine = DatabaseEngineSingleton().engine
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            daños = session.query(Daño).all()
            return daños
        except Exception as e:
            print(f"Error occurred while retrieving Daños: {e}")
            return []
        finally:
            session.close()

    @classmethod
    def get_daños_by_sancion_id(cls, id_sancion: int):
        engine = DatabaseEngineSingleton().engine
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            daños = session.query(Daño).filter(Daño.sancion_id == id_sancion).all()
            daños = [daño.to_dict() for daño in daños]
            return daños
        except Exception as e:
            print(f"Error occurred while retrieving Daños for Sancion {id_sancion}: {e}")
            return []
        finally:
            session.close()

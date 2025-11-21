from estado import Estado
from tipoDaño import TipoDaño
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
    
    def __init__(self, fecha: str, gravedad: int, estado: Estado, tipoDaño: TipoDaño):
        self.fecha = fecha
        self.estado = estado
        self.tipoDaño = tipoDaño

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
        return self.tipoDaño

    def calcularCostoTotal(self):
        return int(self.tipoDaño.getCostoBase() * (1 + self.gravedad / 10))

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
            "id": self.id,
            "fecha": self.fecha,
            "gravedad": self.gravedad,
            "estado": self.estado.to_dict() if self.estado else None,
            "tipoDaño": self.tipoDaño.to_dict() if self.tipoDaño else None
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

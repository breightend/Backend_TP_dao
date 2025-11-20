from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, sessionmaker

from db.base import Base
from db.connection import DatabaseEngineSingleton
from entities.tipoSeguro import TipoSeguro


class Seguro(Base):
    __tablename__ = "Seguros"

    poliza = Column("Poliza", Integer, primary_key=True)
    compañia = Column("Compañia", Integer, nullable=False)
    fechaVencimiento = Column("Fecha_vencimiento", String(10), nullable=False)
    tipoPoliza_id = Column(
        "Tipo_poliza",
        Integer,
        ForeignKey("Tipo_de_seguro.id_tipo_seguro"),
        nullable=False,
    )
    descripcion = Column("Descripcion", String(200), nullable=False)
    costo = Column("Costo", Integer, nullable=False)

    tipoPoliza = relationship(TipoSeguro)

    def __init__(
        self,
        poliza: int,
        compañia: str,
        fechaVencimiento: str,
        tipoPoliza_id: int,
        descripcion: str,
        costo: float,
    ):
        self.poliza = poliza
        self.compañia = compañia
        self.fechaVencimiento = fechaVencimiento
        self.tipoPoliza_id = tipoPoliza_id
        self.descripcion = descripcion
        self.costo = costo

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
    def get_all_seguros(cls):
        engine = DatabaseEngineSingleton().engine

        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            seguros = session.query(Seguro).all()
            seguros_data = [seguro.to_dict() for seguro in seguros]
            return seguros_data
        except Exception as e:
            print(f"Error occurred while retrieving Seguros: {e}")
            return []
        finally:
            session.close()

    @classmethod
    def get_single_seguro(cls, poliza: int):
        engine = DatabaseEngineSingleton().engine

        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            seguro = session.query(Seguro).filter(Seguro.poliza == poliza).first()
            return seguro
        except Exception as e:
            print(f"Error occurred while retrieving Seguro: {e}")

    def to_dict(self):
        return {
            "poliza": self.poliza,
            "compañia": self.compañia,
            "fechaVencimiento": self.fechaVencimiento,
            "tipoPoliza": self.tipoPoliza.to_dict() if self.tipoPoliza else None,
            "descripcion": self.descripcion,
            "costo": self.costo,
        }

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

from db.connection import DatabaseEngineSingleton


class Seguro:
    poliza = Column("Poliza", Integer, primary_key=True)
    compañia = Column("Compañia", Integer, nullable=False)
    fechaVencimiento = Column("fecha_vencimiento", String(10), nullable=False)
    tipoPoliza = Column("tipo_poliza", Integer, nullable=False)
    descripcion = Column("descripcion", String(200), nullable=False)
    costo = Column("costo", Integer, nullable=False)

    def __init__(
        self,
        poliza: int,
        compañia: str,
        fechaVencimiento: str,
        tipoPoliza: int,
        descripcion: str,
        costo: float,
    ):
        self.poliza = poliza
        self.compañia = compañia
        self.fechaVencimiento = fechaVencimiento
        self.tipoPoliza = tipoPoliza
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

    def to_dict(self):
        return {
            "poliza": self.poliza,
            "compañia": self.compañia,
            "fechaVencimiento": self.fechaVencimiento,
            "tipoPoliza": self.tipoPoliza,
            "descripcion": self.descripcion,
            "costo": self.costo,
        }

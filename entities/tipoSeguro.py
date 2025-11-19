from sqlalchemy import Column, Integer
from sqlalchemy.orm import sessionmaker

from db.connection import DatabaseEngineSingleton


class TipoSeguro:
    __tablename__ = "Tipo_Seguro"

    id_tipo_seguro = Column("id_tipo_seguro", Integer, primary_key=True)
    descripcion = Column("descripcion", Integer, nullable=False)

    def __init__(self, id_tipo_seguro: int, descripcion: str):
        self.id_tipo_seguro = id_tipo_seguro
        self.descripcion = descripcion

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
    def get_all_tipo_seguros(cls):
        engine = DatabaseEngineSingleton().engine

        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            tipos_seguros = session.query(TipoSeguro).all()
            tipos_seguros_data = [
                tipo_seguro.to_dict() for tipo_seguro in tipos_seguros
            ]
            return tipos_seguros_data
        except Exception as e:
            print(f"Error occurred while retrieving Tipo_Seguros: {e}")
            return []
        finally:
            session.close()

    def to_dict(self):
        return {
            "id_tipo_seguro": self.id_tipo_seguro,
            "descripcion": self.descripcion,
        }

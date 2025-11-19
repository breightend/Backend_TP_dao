from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from db.base import Base
from db.connection import DatabaseEngineSingleton

class TipoSeguro(Base):
    __tablename__ = "Tipo_de_seguro"

    id_tipo_seguro = Column("id_tipo_seguro", Integer, primary_key=True, autoincrement=True)
    descripcion = Column("descripcion", String, nullable=False)

    def __init__(self, descripcion: str):
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

    @classmethod
    def get_single_tipo_seguro(cls, id_tipo_seguro: int):
        engine = DatabaseEngineSingleton().engine

        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            tipo_seguro = (
                session.query(TipoSeguro)
                .filter(TipoSeguro.id_tipo_seguro == id_tipo_seguro)
                .first()
            )
            return tipo_seguro
        except Exception as e:
            print(f"Error occurred while retrieving Tipo_Seguro: {e}")
            return None
        finally:
            session.close()

    def to_dict(self):
        return {
            "id_tipo_seguro": self.id_tipo_seguro,
            "descripcion": self.descripcion,
        }

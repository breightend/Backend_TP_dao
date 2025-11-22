from db.connection import DatabaseEngineSingleton
from db.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


class TipoSancion(Base):
    __tablename__ = "Tipo_Sancion"
    
    id = Column("id_sancion", Integer, primary_key=True)
    descripcion = Column("descripcion", String(100), nullable=False)

    def __init__(self, descripcion: str):
        self.descripcion = descripcion

    def getDescripcion(self) -> str:
        return self.descripcion

    def setDescripcion(self, descripcion: str):
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

    def to_dict(self):
        return {
            "id": self.id,
            "descripcion": self.descripcion
        }

    @classmethod
    def get_all_tipos_sancion(cls):
        engine = DatabaseEngineSingleton().engine
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            tipos_sancion = session.query(TipoSancion).all()
            tipos_sancion_data = [
                tipo_sancion.to_dict() for tipo_sancion in tipos_sancion
            ]
            return tipos_sancion_data
        except Exception as e:
            print(f"Error occurred while retrieving Tipos de Sancion: {e}")
            return []
        finally:
            session.close()

    @classmethod
    def get_tipo_sancion_by_id(cls, id: int):
        engine = DatabaseEngineSingleton().engine
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            tipo_sancion = session.query(TipoSancion).filter(TipoSancion.id == id).first()
            tipo_sancion_data = tipo_sancion.to_dict() if tipo_sancion else None
            return tipo_sancion_data
        except Exception as e:
            print(f"Error occurred while retrieving Tipo de Sancion: {e}")
            return None
        finally:
            session.close()
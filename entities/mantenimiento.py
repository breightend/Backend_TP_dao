from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker
from db.base import Base
from db.connection import DatabaseEngineSingleton

class Mantenimiento(Base):
    __tablename__ = "Mantenimientos"

    id_mantenimiento = Column("id_mantenimiento", Integer, primary_key=True, autoincrement=True)
    descripcion = Column("descripcion", String(200), nullable=False)
    precio = Column("precio", Float, nullable=False)
    id_orden_mantenimiento = Column("id_orden_mantenimiento", Integer, ForeignKey("Ordenes_de_mantenimiento.id_orden"))

    def __init__(self, descripcion: str, precio: float, id_orden_mantenimiento: int = None):
        self.descripcion = descripcion
        self.precio = precio
        self.id_orden_mantenimiento = id_orden_mantenimiento

    def persist(self):
        engine = DatabaseEngineSingleton().engine
        session_maker = sessionmaker(bind=engine)
        session = session_maker()

        try:
            session.add(self)
            session.commit()
            session.refresh(self)  # Para obtener el id generado
            print(f"Mantenimiento persistido exitosamente: {self.descripcion}")
        except Exception as e:
            session.rollback()
            print(f"Error al persistir mantenimiento: {e}")
            raise e
        finally:
            session.close()

    @classmethod
    def update_mantenimiento(cls, id_mantenimiento: int, descripcion: str, precio: float):
        engine = DatabaseEngineSingleton().engine
        session_maker = sessionmaker(bind=engine)
        session = session_maker()

        try:
            mantenimiento = session.query(cls).filter(cls.id_mantenimiento == id_mantenimiento).first()
            if mantenimiento:
                mantenimiento.descripcion = descripcion
                mantenimiento.precio = precio
                session.commit()
                return mantenimiento
            return None
        except Exception as e:
            session.rollback()
            print(f"Error al actualizar mantenimiento: {e}")
            raise e
        finally:
            session.close()

    @classmethod
    def delete_mantenimiento(cls, id_mantenimiento: int):
        engine = DatabaseEngineSingleton().engine
        session_maker = sessionmaker(bind=engine)
        session = session_maker()

        try:
            mantenimiento = session.query(cls).filter(cls.id_mantenimiento == id_mantenimiento).first()
            if mantenimiento:
                session.delete(mantenimiento)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"Error al eliminar mantenimiento: {e}")
            raise e
        finally:
            session.close()

    def to_dict(self):
        return {
            "id_mantenimiento": self.id_mantenimiento,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "id_orden_mantenimiento": self.id_orden_mantenimiento
        }
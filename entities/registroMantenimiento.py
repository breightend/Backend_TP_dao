from sqlalchemy import Column, Integer, String, ForeignKey, text
from sqlalchemy.orm import relationship, sessionmaker
from db.base import Base
from db.connection import DatabaseEngineSingleton

class RegistroMantenimiento(Base):
    __tablename__ = "Ordenes_de_mantenimiento"

    id_orden = Column("id_orden", Integer, primary_key=True, autoincrement=True)
    fecha_inicio = Column("fecha_inicio", String(10), nullable=False)
    fecha_fin = Column("fecha_fin", String(10), nullable=False)
    patente_vehiculo = Column("patente_vehiculo", String(10), ForeignKey("Automoviles.patente"), nullable=False)

    # Relación con Mantenimientos (One-to-Many)
    mantenimientos = relationship("Mantenimiento", backref="orden", cascade="all, delete-orphan")

    def __init__(self, fecha_inicio: str, fecha_fin: str, patente_vehiculo: str):
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.patente_vehiculo = patente_vehiculo

    def persist(self):
        engine = DatabaseEngineSingleton().engine
        session_maker = sessionmaker(bind=engine)
        session = session_maker()

        try:
            session.add(self)
            session.commit()
            session.refresh(self)  # Para obtener el id_orden generado
            orden_id = self.id_orden
            print(f"Orden de mantenimiento persistida exitosamente: {orden_id}")
            return orden_id
        except Exception as e:
            session.rollback()
            print(f"Error al persistir orden de mantenimiento: {e}")
            raise e
        finally:
            session.close()

    @classmethod
    def get_all_ordenes(cls):
        engine = DatabaseEngineSingleton().engine
        session_maker = sessionmaker(bind=engine)
        session = session_maker()

        try:
            ordenes = session.query(cls).all()
            ordenes_data = []
            
            for orden in ordenes:
                orden_dict = orden.to_dict()
                ordenes_data.append(orden_dict)
            
            return ordenes_data
        except Exception as e:
            print(f"Error al obtener órdenes: {e}")
            return []
        finally:
            session.close()

    @classmethod
    def get_orden_by_id(cls, id_orden: int, objectNeeded: bool):
        engine = DatabaseEngineSingleton().engine
        session_maker = sessionmaker(bind=engine)
        session = session_maker()

        try:
            orden = session.query(cls).filter(cls.id_orden == id_orden).first()
            if orden:
                if objectNeeded:
                    return orden
                # Convertir a dict antes de cerrar la sesión para evitar lazy loading issues
                orden_dict = orden.to_dict()
                return orden_dict
            return None
        except Exception as e:
            print(f"Error al obtener orden {id_orden}: {e}")
            return None
        finally:
            session.close()

    @classmethod
    def delete_orden(cls, id_orden: int):
        engine = DatabaseEngineSingleton().engine
        session_maker = sessionmaker(bind=engine)
        session = session_maker()

        try:
            orden = session.query(cls).filter(cls.id_orden == id_orden).first()
            if orden:
                session.delete(orden)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"Error al eliminar orden: {e}")
            raise e
        finally:
            session.close()

    def to_dict(self):
        # Obtener datos del vehículo manualmente
        vehiculo_data = None
        try:
            engine = DatabaseEngineSingleton().engine
            session_maker = sessionmaker(bind=engine)
            session = session_maker()
            result = session.execute(
                text("SELECT marca, modelo, año FROM Automoviles WHERE patente = :patente"),
                {"patente": self.patente_vehiculo}
            ).fetchone()
            if result:
                vehiculo_data = {
                    "patente": self.patente_vehiculo,
                    "marca": result.marca,
                    "modelo": result.modelo,
                    "anio": result.año
                }
            session.close()
        except Exception as e:
            print(f"Error fetching vehiculo data: {e}")

        return {
            "id_orden": self.id_orden,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "patente_vehiculo": self.patente_vehiculo,
            "vehiculo": vehiculo_data,
            "mantenimientos": [m.to_dict() for m in self.mantenimientos]
        }
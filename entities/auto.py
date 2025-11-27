from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import text
import base64
from sqlalchemy import Column, Integer, String, Float, LargeBinary, ForeignKey
from db.connection import DatabaseEngineSingleton
from db.base import Base


class Auto(Base):
    __tablename__ = "Automoviles"
    
    patente = Column("patente", String, primary_key=True)
    marca = Column("marca", String)
    modelo = Column("modelo", String)
    anio = Column("año", Integer)
    color = Column("color", String)
    costo = Column("precio", Float)
    periodicidadMantenimineto = Column("periocidad_mantenimiento", Integer)
    imagen = Column("imagen", LargeBinary)
    id_estado = Column("id_estado", Integer, ForeignKey("Estados.id_estado"))
    id_seguro = Column("id_seguro", Integer, ForeignKey("Seguros.Poliza"))

    estado = relationship("Estado")
    seguro = relationship("Seguro")

    def __init__(
        self,
        marca: str,
        modelo: str,
        anio: int,
        color: str,
        costo: float,
        patente: str,
        periodicidadMantenimineto: int,
        id_seguro: int,
        imagen: bytes | None = None,
    ):
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.color = color
        self.costo = costo
        self.patente = patente
        self.periodicidadMantenimineto = periodicidadMantenimineto
        self.imagen = imagen
        self.id_estado = 2
        self.id_seguro = id_seguro

    def mostrar_informacion(self):
        return f"{self.marca} {self.modelo}, Año: {self.anio}, Color: {self.color}, Costo: ${self.costo}, Patente: {self.patente}, Periodicidad Mantenimiento: {self.periodicidadMantenimineto} meses"

    def persist(self):
        engine = DatabaseEngineSingleton().engine

        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            session.add(self)
            session.commit()
            print(f"Auto {self.patente} persistido exitosamente")
        except Exception as e:
            session.rollback()
            print(f"Error occurred while persisting Auto: {e}")
            raise e
        finally:
            session.close()
    
    def changeState(self, id_estado: int):
        engine = DatabaseEngineSingleton().engine

        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            session.query(Auto).filter_by(patente=self.patente).update({"id_estado": id_estado})
            session.commit()
            print(f"Auto {self.patente} estado cambiado exitosamente")
        except Exception as e:
            session.rollback()
            print(f"Error occurred while changing state of Auto: {e}")
            raise e
        finally:
            session.close()

    def delete(self):
        from entities.registroAlquilerAuto import RegistroAlquilerAuto
        from entities.registroMantenimiento import RegistroMantenimiento
        engine = DatabaseEngineSingleton().engine

        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            existing_rentals = (
                session.query(RegistroAlquilerAuto)
                .filter_by(patente_vehiculo=self.patente)
                .first()
            )
            if existing_rentals:
                print(
                    f"No se puede eliminar el auto {self.patente} porque tiene alquileres asociados."
                )
                raise ValueError("Auto tiene alquileres asociados")

            existing_maintenance = (
                session.query(RegistroMantenimiento)
                .filter_by(patente_vehiculo=self.patente)
                .first()
            )
            if existing_maintenance:
                print(
                    f"No se puede eliminar el auto {self.patente} porque tiene órdenes de mantenimiento asociadas."
                )
                raise ValueError("Auto tiene órdenes de mantenimiento asociadas")

            # Fetch the object within the current session to ensure it's attached
            auto_to_delete = session.query(Auto).filter_by(patente=self.patente).first()
            if auto_to_delete:
                session.delete(auto_to_delete)
                session.commit()
                print(f"Auto {self.patente} eliminado exitosamente")
            else:
                print(f"Auto {self.patente} no encontrado para eliminar")

        except Exception as e:
            session.rollback()
            print(f"Error occurred while deleting Auto: {e}")
            raise e
        finally:
            session.close()

    @classmethod
    def get_autos_states(cls):
        from .estado import Estado
        return Estado.get_all_estados_de_ambito("Automoviles")

    @classmethod
    def get_all_autos(cls):
        engine = DatabaseEngineSingleton().engine

        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            autos = session.query(cls).all()

            autos_data = []
            for auto in autos:
                imagen_bytes = auto.imagen
                imagen_b64 = None
                if imagen_bytes:
                    try:
                        imagen_b64 = base64.b64encode(imagen_bytes).decode("utf-8")
                    except Exception:
                        imagen_b64 = None

                auto_dict = {
                    "patente": auto.patente,
                    "marca": auto.marca,
                    "modelo": auto.modelo,
                    "anio": auto.anio,
                    "color": auto.color,
                    "costo": auto.costo,
                    "periodicidadMantenimineto": auto.periodicidadMantenimineto,
                    "imagen": imagen_b64,
                    "estado": auto.estado.nombre,
                }
                autos_data.append(auto_dict)
            return autos_data
        except Exception as e:
            print(f"Error occurred while retrieving autos: {e}")
            return []
        finally:
            session.close()
            return autos_data

    def to_dict(self):
        return {
            "patente": self.patente,
            "marca": self.marca,
            "modelo": self.modelo,
            "anio": self.anio,
            "color": self.color,
            "costo": self.costo,
            "periodicidadMantenimineto": self.periodicidadMantenimineto,
            "estado": self.estado.to_dict(),    
            "seguro": self.seguro.to_dict(),
        }

    @classmethod
    def get_auto_by_patente(cls, patente: str):
        from sqlalchemy.orm import joinedload
        from entities.seguro import Seguro

        engine = DatabaseEngineSingleton().engine
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            auto = session.query(cls).options(
                joinedload(cls.estado),
                joinedload(cls.seguro).joinedload(Seguro.tipoPoliza)
            ).filter_by(patente=patente).first()
            return auto
        except Exception as e:
            print(f"Error occurred while retrieving Auto: {e}")
            return None
        finally:
            session.close()

    @classmethod
    def get_autos_available(cls):
        from sqlalchemy.orm import joinedload
        from entities.seguro import Seguro
        engine = DatabaseEngineSingleton().engine

        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            autos = session.query(cls).options(
                joinedload(cls.estado), 
                joinedload(cls.seguro).joinedload(Seguro.tipoPoliza)
            ).filter_by(id_estado=2).all()
            return autos
        except Exception as e:
            print(f"Error occurred while retrieving autos: {e}")
            return []
        finally:
            session.close()

    @classmethod
    def get_autos_available_for_rental(cls, fecha_inicio: str = None, fecha_fin: str = None):
        from sqlalchemy.orm import joinedload
        from entities.seguro import Seguro
        from entities.registroAlquilerAuto import RegistroAlquilerAuto
        engine = DatabaseEngineSingleton().engine

        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            autos = session.query(cls).options(
                joinedload(cls.estado), 
                joinedload(cls.seguro).joinedload(Seguro.tipoPoliza)
            ).filter_by(id_estado=2).all()

            if fecha_inicio and fecha_fin:
                autos_disponibles = []
                for auto in autos:
                    if RegistroAlquilerAuto.car_available(auto.patente, fecha_inicio, fecha_fin):
                        autos_disponibles.append(auto)
                return autos_disponibles
            
            return autos
        except Exception as e:
            print(f"Error occurred while retrieving autos: {e}")
            return []
        finally:
            session.close()

    @classmethod
    def get_auto_by_patente_with_details(cls, patente: str):
        """
        Obtiene toda la información de un auto específico incluyendo:
        - Información básica del auto
        - Estado actual
        - Información del seguro
        - Historial de alquileres
        - Historial de mantenimientos
        """
        from entities.registroAlquilerAuto import RegistroAlquilerAuto
        from entities.registroMantenimiento import RegistroMantenimiento
        from entities.sancion import Sancion
        from entities.seguro import Seguro
        from sqlalchemy.orm import joinedload

        engine = DatabaseEngineSingleton().engine
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            # 1. Obtener auto con estado y seguro
            auto = session.query(cls).options(
                joinedload(cls.estado),
                joinedload(cls.seguro).joinedload(Seguro.tipoPoliza)
            ).filter_by(patente=patente).first()

            if not auto:
                return None

            # Convertir imagen a base64
            imagen_b64 = None
            if auto.imagen:
                try:
                    imagen_b64 = base64.b64encode(auto.imagen).decode("utf-8")
                except Exception:
                    imagen_b64 = None

            # 2. Obtener historial de alquileres
            alquileres = session.query(RegistroAlquilerAuto).options(
                joinedload(RegistroAlquilerAuto.cliente),
                joinedload(RegistroAlquilerAuto.empleado)
            ).filter_by(patente_vehiculo=patente).order_by(RegistroAlquilerAuto.fechaInicio.desc()).all()

            alquileres_data = []
            for alq in alquileres:
                # Obtener sanciones para cada alquiler
                sanciones = session.query(Sancion).options(
                    joinedload(Sancion.tipo_sancion)
                ).filter_by(id_alquiler=alq.id).all()

                sanciones_data = [
                    {
                        "id_sancion": s.id,
                        "precio": s.costo_base,
                        "descripcion": s.descripcion,
                        "tipo_descripcion": s.tipo_sancion.descripcion if s.tipo_sancion else None,
                    }
                    for s in sanciones
                ]

                alquileres_data.append({
                    "id_alquiler": alq.id,
                    "precio": alq.precio,
                    "fecha_inicio": alq.fechaInicio,
                    "fecha_fin": alq.fechaFin,
                    "cliente": {
                        "dni": alq.cliente.dni,
                        "nombre": alq.cliente.nombre,
                        "apellido": alq.cliente.apellido,
                        "email": alq.cliente.email,
                    } if alq.cliente else None,
                    "empleado": {
                        "legajo": alq.empleado.legajo,
                        "nombre": alq.empleado.nombre,
                        "apellido": alq.empleado.apellido,
                    } if alq.empleado else None,
                    "sanciones": sanciones_data,
                })

            # 3. Obtener historial de mantenimientos
            ordenes = session.query(RegistroMantenimiento).options(
                joinedload(RegistroMantenimiento.mantenimientos)
            ).filter_by(patente_vehiculo=patente).order_by(RegistroMantenimiento.fecha_inicio.desc()).all()

            mantenimientos_data = []
            for orden in ordenes:
                mants = [
                    {
                        "id_mantenimiento": m.id_mantenimiento,
                        "precio": m.precio,
                        "descripcion": m.descripcion,
                    }
                    for m in orden.mantenimientos
                ]
                
                mantenimientos_data.append({
                    "id_orden": orden.id_orden,
                    "fecha_inicio": orden.fecha_inicio,
                    "fecha_fin": orden.fecha_fin,
                    "mantenimientos": mants,
                })

            # Construir respuesta completa
            auto_completo = {
                "patente": auto.patente,
                "marca": auto.marca,
                "modelo": auto.modelo,
                "anio": auto.anio,
                "color": auto.color,
                "costo": auto.costo,
                "periodicidadMantenimineto": auto.periodicidadMantenimineto,
                "imagen": imagen_b64,
                "estado": {
                    "nombre": auto.estado.nombre if auto.estado else None,
                    "ambito": auto.estado.ambito if auto.estado else None,
                },
                "seguro": {
                    "descripcion": auto.seguro.descripcion if auto.seguro else None,
                    "costo": auto.seguro.costo if auto.seguro else None,
                    "tipo_descripcion": auto.seguro.tipoPoliza.descripcion if auto.seguro and auto.seguro.tipoPoliza else None,
                },
                "historial_alquileres": alquileres_data,
                "historial_mantenimientos": mantenimientos_data,
            }

            return auto_completo

        except Exception as e:
            print(f"Error occurred while retrieving auto details: {e}")
            return None
        finally:
            session.close()

from calendar import c

from sqlalchemy.orm import sessionmaker

from db.connection import DatabaseEngineSingleton
from entities.persona import Persona


class Cliente(Persona):
    __tablename__ = "Clientes"

    __mapper_args__ = {
        "polymorphic_identity": "cliente",
    }

    def __init__(
        self,
        nombre: str,
        apellido: str,
        direccion: str,
        fechaNacimiento: str,
        dni: str,
        telefono: str,
        email: str,
    ):
        super().__init__(
            nombre, apellido, direccion, fechaNacimiento, dni, telefono, email
        )

    def mostrar_informacion(self):
        return super().mostrar_informacion()

    def persist(self):
        engine = DatabaseEngineSingleton().engine

        Session = sessionmaker(bind=engine)
        session = Session()

        session.add(self)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error occurred while persisting Cliente: {e}")
        finally:
            session.close()
    
    def delete(self):
        from entities.registroAlquilerAuto import RegistroAlquilerAuto
        engine = DatabaseEngineSingleton().engine

        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            existing_rentals = (
                session.query(RegistroAlquilerAuto)
                .filter_by(dni_cliente=self.dni)
                .first()
            )
            if existing_rentals:
                print(
                    f"No se puede eliminar el cliente {self.dni} porque tiene alquileres asociados."
                )
                return

            # Fetch the object within the current session to ensure it's attached
            client_to_delete = session.query(Cliente).filter_by(dni=self.dni).first()
            if client_to_delete:
                session.delete(client_to_delete)
                session.commit()
                print(f"Cliente {self.dni} eliminado exitosamente")
            else:
                print(f"Cliente {self.dni} no encontrado para eliminar")

        except Exception as e:
            session.rollback()
            print(f"Error occurred while deleting Cliente: {e}")
            raise e
        finally:
            session.close()

    @classmethod
    def get_all_clients(cls):
        engine = DatabaseEngineSingleton().engine

        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            clients = session.query(Cliente).all()
            clients_data = [client.to_dict() for client in clients]
            return clients_data
        except Exception as e:
            print(f"Error occurred while retrieving clients: {e}")
            return []
        finally:
            session.close()

    @classmethod
    def get_client_by_dni(cls, dni):
        engine = DatabaseEngineSingleton().engine

        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            client = session.query(Cliente).filter_by(dni=dni).first()
            return client
        except Exception as e:
            print(f"Error occurred while retrieving client by DNI: {e}")
            return None
        finally:
            session.close()

    def to_dict(self):
        return {
            "dni_cliente": self.dni,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "direccion": self.direccion,
            "email": self.email,
            "telefono": self.telefono,
            "fechaNacimiento": self.fechaNacimiento,
        }

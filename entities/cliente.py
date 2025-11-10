from entities.persona import Persona
from sqlalchemy.orm import sessionmaker
from db.connection import DatabaseEngineSingleton
class Cliente(Persona):

    __tablename__ = "Clientes"

    __mapper_args__ = {
        'polymorphic_identity': 'cliente',
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
        super().__init__(nombre, apellido, direccion, fechaNacimiento, dni, telefono, email)
    

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



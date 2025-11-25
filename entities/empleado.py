from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import sessionmaker

from db.connection import DatabaseEngineSingleton
from entities.persona import Persona


class Empleado(Persona):
    __tablename__ = "Empleados"

    __mapper_args__ = {
        "polymorphic_identity": "empleado",
    }

    legajo = Column("legajo", Integer, primary_key=True)
    puesto = Column("puesto", String(200), nullable=False)
    salario = Column("salario", Float, nullable=False)
    fechaInicioActividad = Column("fecha_inicio_actividad", String(100), nullable=False)
    dni = Column("dni", Integer)

    def __init__(
        self,
        nombre: str,
        apellido: str,
        direccion: str,
        fechaNacimiento: str,
        dni: str,
        telefono: str,
        email: str,
        legajo: str,
        puesto: str,
        salario: float,
        fechaInicioActividad: str,
    ):
        super().__init__(
            nombre, apellido, direccion, fechaNacimiento, dni, telefono, email
        )
        self.legajo = legajo
        self.puesto = puesto
        self.salario = salario
        self.fechaInicioActividad = fechaInicioActividad

    def get_description(self) -> str:
        return (
            f"Empleado ID: {self.legajo}, Nombre: {self.nombre} {self.apellido}, "
            f"Puesto: {self.puesto}"
            f"Fecha de Inicio de Actividad: {self.fechaInicioActividad}"
        )

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

    @staticmethod
    def get_all_employees():
        engine = DatabaseEngineSingleton().engine

        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            empleados = session.query(Empleado).all()

            empleados_data = [empleado.to_dict() for empleado in empleados]

            return empleados_data
        except Exception as e:
            print(f"Error occurred while fetching Empleados: {e}")
            return []
        finally:
            session.close()

    @classmethod
    def get_employee_by_dni(cls, dni):
        engine = DatabaseEngineSingleton().engine
        Session = sessionmaker(bind=engine)

        with Session() as session:
            try:
                empleado = session.query(Empleado).filter_by(dni=dni).first()
                return empleado
            except Exception as e:
                print(f"Error occurred while retrieving empleado by DNI: {e}")
                return None

    def to_dict(self) -> dict:
        return {
            "legajo_empleado": self.legajo,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "direccion": self.direccion,
            "fechaNacimiento": self.fechaNacimiento,
            "DNI": self.dni,
            "telefono": self.telefono,
            "email": self.email,
            "puesto": self.puesto,
            "salario": self.salario,
            "fechaInicioActividad": self.fechaInicioActividad,
        }

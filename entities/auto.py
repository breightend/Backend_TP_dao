from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import base64

from db.connection import DatabaseEngineSingleton


class Auto:
    marca: str
    modelo: str
    anio: int
    color: str
    costo: float
    patente: str
    periodicidadMantenimineto: int
    imagen: bytes | None

    def __init__(
        self,
        marca: str,
        modelo: str,
        anio: int,
        color: str,
        costo: float,
        patente: str,
        periodicidadMantenimineto: int,
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

    def mostrar_informacion(self):
        return f"{self.marca} {self.modelo}, Año: {self.anio}, Color: {self.color}, Costo: ${self.costo}, Patente: {self.patente}, Periodicidad Mantenimiento: {self.periodicidadMantenimineto} meses"

    def persist(self):
        engine = DatabaseEngineSingleton().engine

        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            # Insertar el auto en la tabla Automoviles
            query = text("""
                INSERT INTO Automoviles (patente, marca, modelo, año, color, precio, periocidad_mantenimiento, imagen, id_estado, id_seguro)
                VALUES (:patente, :marca, :modelo, :anio, :color, :precio, :periodicidad, :imagen, 1, 1)
            """)

            session.execute(
                query,
                {
                    "patente": self.patente,
                    "marca": self.marca,
                    "modelo": self.modelo,
                    "anio": self.anio,
                    "color": self.color,
                    "precio": self.costo,
                    "periodicidad": self.periodicidadMantenimineto,
                    "imagen": self.imagen,
                },
            )

            session.commit()
            print(f"Auto {self.patente} persistido exitosamente")
        except Exception as e:
            session.rollback()
            print(f"Error occurred while persisting Auto: {e}")
            raise e
        finally:
            session.close()

    @classmethod
    def get_all_autos(cls):
        engine = DatabaseEngineSingleton().engine

        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            query = text("SELECT * FROM Automoviles")
            result = session.execute(query)

            autos_data = []
            for row in result:
                imagen_bytes = getattr(row, "imagen", None)
                imagen_b64 = None
                if imagen_bytes:
                    try:
                        imagen_b64 = base64.b64encode(imagen_bytes).decode("utf-8")
                    except Exception:
                        imagen_b64 = None

                auto_dict = {
                    "patente": row.patente,
                    "marca": row.marca,
                    "modelo": row.modelo,
                    "anio": row.año,
                    "color": row.color,
                    "costo": row.precio,
                    "periodicidadMantenimineto": row.periocidad_mantenimiento,
                    "imagen": imagen_b64,
                }
                autos_data.append(auto_dict)

            return autos_data
        except Exception as e:
            print(f"Error occurred while retrieving autos: {e}")
            return []
        finally:
            session.close()

    def to_dict(self):
        return {
            "patente": self.patente,
            "marca": self.marca,
            "modelo": self.modelo,
            "anio": self.anio,
            "color": self.color,
            "costo": self.costo,
            "periodicidadMantenimineto": self.periodicidadMantenimineto,
            "imagen": base64.b64encode(self.imagen).decode("utf-8")
            if self.imagen
            else None,
        }

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
        engine = DatabaseEngineSingleton().engine
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            # Consulta principal para obtener información del auto con estado y seguro
            main_query = text("""
                SELECT 
                    a.patente, a.marca, a.modelo, a.año, a.color, a.precio, 
                    a.periocidad_mantenimiento, a.imagen,
                    e.nombre as estado_nombre, e.ambito as estado_ambito,
                    s.descripcion as seguro_descripcion, s.costo as seguro_costo,
                    ts.descripcion as tipo_seguro_descripcion
                FROM Automoviles a
                LEFT JOIN Estados e ON a.id_estado = e.id_estado
                LEFT JOIN Seguros s ON a.id_seguro = s.id_seguro
                LEFT JOIN Tipo_de_seguro ts ON s.id_tipo_seguro = ts.id_tipo_seguro
                WHERE a.patente = :patente
            """)

            result = session.execute(main_query, {"patente": patente}).fetchone()

            if not result:
                return None

            # Convertir imagen a base64 si existe
            imagen_b64 = None
            if result.imagen:
                try:
                    imagen_b64 = base64.b64encode(result.imagen).decode("utf-8")
                except Exception:
                    imagen_b64 = None

            # Obtener historial de alquileres
            alquileres_query = text("""
                SELECT 
                    al.id_alquiler, al.precio, al.fecha_inicio, al.fecha_fin,
                    c.dni as cliente_dni, c.nombre as cliente_nombre, 
                    c.apellido as cliente_apellido, c.email as cliente_email,
                    e.legajo as empleado_legajo, e.nombre as empleado_nombre,
                    e.apellido as empleado_apellido
                FROM Alquileres_de_auto al
                LEFT JOIN Clientes c ON al.dni_cliente = c.dni
                LEFT JOIN Empleados e ON al.legajo_empleado = e.legajo
                WHERE al.patente_vehiculo = :patente
                ORDER BY al.fecha_inicio DESC
            """)

            alquileres_result = session.execute(
                alquileres_query, {"patente": patente}
            ).fetchall()

            # Obtener sanciones para cada alquiler
            alquileres_data = []
            for alquiler in alquileres_result:
                sanciones_query = text("""
                    SELECT 
                        s.id_sancion, s.precio, s.descripcion,
                        ts.descripcion as tipo_descripcion
                    FROM Sanciones s
                    LEFT JOIN Tipo_Sancion ts ON s.id_tipo_sancion = ts.id_sancion
                    WHERE s.id_alquiler = :id_alquiler
                """)

                sanciones_result = session.execute(
                    sanciones_query, {"id_alquiler": alquiler.id_alquiler}
                ).fetchall()

                sanciones_data = [
                    {
                        "id_sancion": sancion.id_sancion,
                        "precio": sancion.precio,
                        "descripcion": sancion.descripcion,
                        "tipo_descripcion": sancion.tipo_descripcion,
                    }
                    for sancion in sanciones_result
                ]

                alquiler_data = {
                    "id_alquiler": alquiler.id_alquiler,
                    "precio": alquiler.precio,
                    "fecha_inicio": alquiler.fecha_inicio,
                    "fecha_fin": alquiler.fecha_fin,
                    "cliente": {
                        "dni": alquiler.cliente_dni,
                        "nombre": alquiler.cliente_nombre,
                        "apellido": alquiler.cliente_apellido,
                        "email": alquiler.cliente_email,
                    },
                    "empleado": {
                        "legajo": alquiler.empleado_legajo,
                        "nombre": alquiler.empleado_nombre,
                        "apellido": alquiler.empleado_apellido,
                    },
                    "sanciones": sanciones_data,
                }
                alquileres_data.append(alquiler_data)

            # Obtener historial de mantenimientos
            mantenimientos_query = text("""
                SELECT 
                    om.id_orden, om.fecha_inicio, om.fecha_fin,
                    m.id_mantenimiento, m.precio, m.descripcion
                FROM Ordenes_de_mantenimiento om
                LEFT JOIN Mantenimientos m ON om.id_orden = m.id_orden_mantenimiento
                WHERE om.patente_vehiculo = :patente
                ORDER BY om.fecha_inicio DESC
            """)

            mantenimientos_result = session.execute(
                mantenimientos_query, {"patente": patente}
            ).fetchall()

            # Agrupar mantenimientos por orden
            ordenes_mantenimiento = {}
            for row in mantenimientos_result:
                orden_id = row.id_orden
                if orden_id not in ordenes_mantenimiento:
                    ordenes_mantenimiento[orden_id] = {
                        "id_orden": orden_id,
                        "fecha_inicio": row.fecha_inicio,
                        "fecha_fin": row.fecha_fin,
                        "mantenimientos": [],
                    }

                if row.id_mantenimiento:  # Si hay mantenimiento asociado
                    ordenes_mantenimiento[orden_id]["mantenimientos"].append(
                        {
                            "id_mantenimiento": row.id_mantenimiento,
                            "precio": row.precio,
                            "descripcion": row.descripcion,
                        }
                    )

            mantenimientos_data = list(ordenes_mantenimiento.values())

            # Construir respuesta completa
            auto_completo = {
                "patente": result.patente,
                "marca": result.marca,
                "modelo": result.modelo,
                "anio": result.año,
                "color": result.color,
                "costo": result.precio,
                "periodicidadMantenimineto": result.periocidad_mantenimiento,
                "imagen": imagen_b64,
                "estado": {
                    "nombre": result.estado_nombre,
                    "ambito": result.estado_ambito,
                },
                "seguro": {
                    "descripcion": result.seguro_descripcion,
                    "costo": result.seguro_costo,
                    "tipo_descripcion": result.tipo_seguro_descripcion,
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

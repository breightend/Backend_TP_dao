from connection import DatabaseEngineSingleton
from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    LargeBinary,
)

meta = MetaData()

engine = DatabaseEngineSingleton().engine


estados = Table(
    "Estados",
    meta,
    Column("id_estado", Integer, primary_key=True),
    Column("nombre", String(50), nullable=False),
    Column("ambito", String(50), nullable=False),
)

clientes = Table(
    "Clientes",
    meta,
    Column("dni", Integer, primary_key=True, autoincrement=False),
    Column("direccion", String(200), nullable=False),
    Column("nombre", String(100), nullable=False),
    Column("apellido", String(100), nullable=False),
    Column("email", String(100), nullable=False),
    Column("telefono", String(20), nullable=False),
    Column("fecha_nacimiento", String(10), nullable=False),
)

empleados = Table(
    "Empleados",
    meta,
    Column("legajo", Integer, primary_key=True),
    Column("dni", Integer, nullable=False),
    Column("nombre", String(100), nullable=False),
    Column("apellido", String(100), nullable=False),
    Column("direccion", String(200), nullable=False),
    Column("email", String(100), nullable=False),
    Column("telefono", String(20), nullable=False),
    Column("fecha_nacimiento", String(10), nullable=False),
    Column("puesto", String(100), nullable=False),
    Column("fecha_inicio_actividad", String(10), nullable=False),
    Column("salario", Float, nullable=False),
)

tipo_sancion = Table(
    "Tipo_Sancion",
    meta,
    Column("id_sancion", Integer, primary_key=True),
    Column("descripcion", String(200), nullable=False),
)

alquileres = Table(
    "Alquileres_de_auto",
    meta,
    Column("id_alquiler", Integer, primary_key=True),
    Column("patente_vehiculo", String(10), ForeignKey("Automoviles.patente")),
    Column("dni_cliente", Integer, ForeignKey("Clientes.dni")),
    Column("legajo_empleado", Integer, ForeignKey("Empleados.legajo")),
    Column("precio", Float, nullable=False),
    Column("fecha_inicio", String(10), nullable=False),
    Column("fecha_fin", String(10), nullable=False),
)

sanciones = Table(
    "Sanciones",
    meta,
    Column("id_sancion", Integer, primary_key=True),
    Column("id_alquiler", Integer, ForeignKey("Alquileres_de_auto.id_alquiler")),
    Column("precio", Float, nullable=False),
    Column("descripcion", String(200), nullable=False),
    Column("id_tipo_sancion", Integer, ForeignKey("Tipo_Sancion.id_sancion")),
)

mantenimientos = Table(
    "Mantenimientos",
    meta,
    Column("id_mantenimiento", Integer, primary_key=True),
    Column(
        "id_orden_mantenimiento",
        Integer,
        ForeignKey("Ordenes_de_mantenimiento.id_orden"),
    ),
    Column("precio", Float, nullable=False),
    Column("descripcion", String(200), nullable=False),
)

ordenes_mantenimiento = Table(
    "Ordenes_de_mantenimiento",
    meta,
    Column("id_orden", Integer, primary_key=True),
    Column("patente_vehiculo", String(10), ForeignKey("Automoviles.patente")),
    Column("fecha_inicio", String(10), nullable=False),
    Column("fecha_fin", String(10), nullable=False),
)

automoviles = Table(
    "Automoviles",
    meta,
    Column("patente", String(10), primary_key=True),
    Column("marca", String(50), nullable=False),
    Column("modelo", String(50), nullable=False),
    Column("año", Integer, nullable=False),
    Column("color", String(50), nullable=False),
    Column("precio", Float, nullable=False),
    Column("periocidad_mantenimiento", Integer, nullable=False),
    Column("imagen", LargeBinary, nullable=True),
    Column("id_estado", Integer, ForeignKey("Estados.id_estado")),
    Column("id_seguro", Integer, ForeignKey("Seguros.poliza")),
)

tipo_seguro = Table(
    "Tipo_de_seguro",
    meta,
    Column("id_tipo_seguro", Integer, primary_key=True),
    Column("descripcion", String(200), nullable=False),
)

seguros = Table(
    "Seguros",
    meta,
    Column("poliza", Integer, primary_key=True),
    Column("compañia", String(200), nullable=False),
    Column("fecha_vencimiento", String(10), nullable=False),
    Column("tipo_poliza", Integer, ForeignKey("Tipo_de_seguro.id_tipo_seguro")),
    Column("descripcion", String(10), nullable=False),
    Column("costo", Float, nullable=False),
)

tipo_daño = Table(
    "Tipo_de_daño",
    meta,
    Column("id_daño", Integer, primary_key=True),
    Column("nombre", String(100), nullable=False),
)

meta.create_all(engine)

from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime

meta = MetaData()


tabla_clientes = Table(
    "Clientes",
    meta,
    Column("dni", Integer, primary_key=True),
    Column("tipo_documento", String(100), pr=False),
    Column("direccion", String(200), nullable=False),
    Column("nombre", String(100), nullable=False),
    Column("apellido", String(100), nullable=False),
    Column("email", String(100), nullable=False),
    Column("telefono", String(20), nullable=False),
    Column("fecha_nacimiento", DateTime, nullable=False)
)


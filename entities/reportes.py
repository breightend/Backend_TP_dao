from collections import defaultdict
from contextlib import contextmanager
from typing import Any, Dict, Iterator, List, Optional, Tuple

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import text

from db.connection import DatabaseEngineSingleton


SessionFactory = sessionmaker(bind=DatabaseEngineSingleton().engine)


@contextmanager
def session_scope() -> Iterator[Session]:
    """Provide a transactional scope around a series of operations."""
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()


## utils

# Arma la cláusula de fechas y parámetros asociados.
def _build_date_filters(
    fecha_desde: Optional[str], fecha_hasta: Optional[str]
) -> Tuple[str, Dict[str, Any]]:
    filtros: List[str] = []
    params: Dict[str, Any] = {}

    if fecha_desde:
        filtros.append("al.fecha_inicio >= :fecha_desde")
        params["fecha_desde"] = fecha_desde

    if fecha_hasta:
        filtros.append("al.fecha_inicio <= :fecha_hasta")
        params["fecha_hasta"] = fecha_hasta

    if filtros:
        return " AND ".join(filtros), params

    return "", params


## reports

# Devuelve alquileres detallados y un resumen agregado por cliente.
def get_alquileres_detallados(
    dni: Optional[str] = None,
    fecha_desde: Optional[str] = None,
    fecha_hasta: Optional[str] = None,
) -> Dict[str, Any]:
    filtros_where: List[str] = []
    params: Dict[str, Any] = {}

    if dni:
        filtros_where.append("al.dni_cliente = :dni")
        params["dni"] = dni

    filtro_fechas, params_fechas = _build_date_filters(fecha_desde, fecha_hasta)
    if filtro_fechas:
        filtros_where.append(f"({filtro_fechas})")
        params.update(params_fechas)

    where_clause = ""
    if filtros_where:
        where_clause = "WHERE " + " AND ".join(filtros_where)

    alquileres_query = text(
        f"""
        SELECT
            al.id_alquiler,
            al.fecha_inicio,
            al.fecha_fin,
            al.precio AS precio_base,
            al.dni_cliente,
            al.patente_vehiculo,
            c.nombre AS cliente_nombre,
            c.apellido AS cliente_apellido,
            c.email AS cliente_email,
            a.marca,
            a.modelo,
            a.año,
            IFNULL(s.total_sanciones, 0) AS total_sanciones
        FROM Alquileres_de_auto al
        JOIN Clientes c ON al.dni_cliente = c.dni
        JOIN Automoviles a ON a.patente = al.patente_vehiculo
        LEFT JOIN (
            SELECT id_alquiler, SUM(costo_base) AS total_sanciones
            FROM Sanciones
            GROUP BY id_alquiler
        ) s ON s.id_alquiler = al.id_alquiler
        {where_clause}
        ORDER BY al.fecha_inicio DESC
        """
    )

    sanciones_query = text(
        """
        SELECT id_sancion, costo_base AS precio, descripcion, id_tipo_sancion
        FROM Sanciones
        WHERE id_alquiler = :id_alquiler
        """
    )

    alquileres: List[Dict[str, Any]] = []
    resumen_por_cliente: Dict[str, Dict[str, Any]] = defaultdict(
        lambda: {
            "dni": "",
            "nombre": "",
            "apellido": "",
            "cantidad_alquileres": 0,
            "total_alquileres": 0.0,
            "total_sanciones": 0.0,
            "total_general": 0.0,
        }
    )

    with session_scope() as session:
        alquileres_result = session.execute(alquileres_query, params).fetchall()

        for row in alquileres_result:
            sanciones_result = session.execute(
                sanciones_query, {"id_alquiler": row.id_alquiler}
            ).fetchall()

            sanciones = [
                {
                    "id_sancion": sancion.id_sancion,
                    "precio": sancion.precio,
                    "descripcion": sancion.descripcion,
                    "id_tipo_sancion": sancion.id_tipo_sancion,
                }
                for sancion in sanciones_result
            ]

            total_sanciones = float(row.total_sanciones or 0)
            total_general = float(row.precio_base or 0) + total_sanciones

            alquileres.append(
                {
                    "id_alquiler": row.id_alquiler,
                    "fecha_inicio": row.fecha_inicio,
                    "fecha_fin": row.fecha_fin,
                    "precio_base": float(row.precio_base or 0),
                    "total_sanciones": total_sanciones,
                    "total_general": total_general,
                    "cliente": {
                        "dni": row.dni_cliente,
                        "nombre": row.cliente_nombre,
                        "apellido": row.cliente_apellido,
                        "email": row.cliente_email,
                    },
                    "vehiculo": {
                        "patente": row.patente_vehiculo,
                        "marca": row.marca,
                        "modelo": row.modelo,
                        "anio": row.año,
                    },
                    "sanciones": sanciones,
                }
            )

            cliente_key = str(row.dni_cliente)
            resumen = resumen_por_cliente[cliente_key]
            resumen["dni"] = row.dni_cliente
            resumen["nombre"] = row.cliente_nombre
            resumen["apellido"] = row.cliente_apellido
            resumen["cantidad_alquileres"] += 1
            resumen["total_alquileres"] += float(row.precio_base or 0)
            resumen["total_sanciones"] += total_sanciones
            resumen["total_general"] += total_general

    resumen_ordenado = sorted(
        resumen_por_cliente.values(),
        key=lambda item: item["cantidad_alquileres"],
        reverse=True,
    )

    return {
        "alquileres": alquileres,
        "resumen_clientes": resumen_ordenado,
    }


# Devuelve un ranking de vehículos según cantidad de alquileres.
def get_vehiculos_mas_alquilados(
    fecha_desde: Optional[str] = None,
    fecha_hasta: Optional[str] = None,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    filtro_fechas, params = _build_date_filters(fecha_desde, fecha_hasta)
    where_clause = f"WHERE {filtro_fechas}" if filtro_fechas else ""

    query = text(
        f"""
        SELECT
            a.patente,
            a.marca,
            a.modelo,
            a.año,
            COUNT(al.id_alquiler) AS cantidad_alquileres
        FROM Alquileres_de_auto al
        JOIN Automoviles a ON a.patente = al.patente_vehiculo
        {where_clause}
        GROUP BY a.patente, a.marca, a.modelo, a.año
        ORDER BY cantidad_alquileres DESC, a.patente
        LIMIT :limit
        """
    )

    params["limit"] = max(limit, 1)

    with session_scope() as session:
        resultados = session.execute(query, params).fetchall()

    return [
        {
            "patente": row.patente,
            "marca": row.marca,
            "modelo": row.modelo,
            "anio": row.año,
            "cantidad_alquileres": row.cantidad_alquileres,
        }
        for row in resultados
    ]


# Agrupa alquileres por mes o por trimestre.
def get_alquileres_por_periodo(
    periodicidad: str = "mes",
    fecha_desde: Optional[str] = None,
    fecha_hasta: Optional[str] = None,
) -> List[Dict[str, Any]]:
    periodicidad = periodicidad.lower()
    if periodicidad not in {"mes", "trimestre"}:
        periodicidad = "mes"

    filtro_fechas, params = _build_date_filters(fecha_desde, fecha_hasta)
    where_clause = f"WHERE {filtro_fechas}" if filtro_fechas else ""

    if periodicidad == "mes":
        periodo_expr = "strftime('%Y-%m', al.fecha_inicio)"
    else:
        periodo_expr = (
            "strftime('%Y', al.fecha_inicio) || '-Q' || "
            "CAST(((CAST(strftime('%m', al.fecha_inicio) AS INTEGER) - 1) / 3) + 1 AS INTEGER)"
        )

    query = text(
        f"""
        SELECT
            {periodo_expr} AS periodo,
            COUNT(al.id_alquiler) AS cantidad_alquileres,
            SUM(al.precio) AS total_alquileres
        FROM Alquileres_de_auto al
        {where_clause}
        GROUP BY periodo
        ORDER BY periodo
        """
    )

    with session_scope() as session:
        resultados = session.execute(query, params).fetchall()

    return [
        {
            "periodo": row.periodo,
            "cantidad_alquileres": row.cantidad_alquileres,
            "total_alquileres": float(row.total_alquileres or 0),
        }
        for row in resultados
    ]


# Calcula la facturación mensual considerando alquileres y sanciones.
def get_facturacion_mensual(
    fecha_desde: Optional[str] = None,
    fecha_hasta: Optional[str] = None,
    incluir_sanciones: bool = True,
) -> Dict[str, Any]:
    filtro_fechas, params = _build_date_filters(fecha_desde, fecha_hasta)
    where_clause = f"WHERE {filtro_fechas}" if filtro_fechas else ""

    query = text(
        f"""
        WITH alquileres_filtrados AS (
            SELECT al.id_alquiler, al.precio, al.fecha_inicio
            FROM Alquileres_de_auto al
            {where_clause}
        ), sanciones_por_alquiler AS (
            SELECT id_alquiler, SUM(costo_base) AS total_sanciones
            FROM Sanciones
            GROUP BY id_alquiler
        )
        SELECT
            strftime('%Y-%m', af.fecha_inicio) AS periodo,
            SUM(af.precio) AS total_alquileres,
            IFNULL(SUM(spa.total_sanciones), 0) AS total_sanciones
        FROM alquileres_filtrados af
        LEFT JOIN sanciones_por_alquiler spa ON spa.id_alquiler = af.id_alquiler
        GROUP BY periodo
        ORDER BY periodo
        """
    )

    with session_scope() as session:
        resultados = session.execute(query, params).fetchall()

    periodos: List[Dict[str, Any]] = []
    acumulados = {
        "total_alquileres": 0.0,
        "total_sanciones": 0.0,
        "total_descuentos": 0.0,
        "total_general": 0.0,
    }

    for row in resultados:
        total_alquileres = float(row.total_alquileres or 0)
        total_sanciones = float(row.total_sanciones or 0)
        total_descuentos = 0.0

        total_general = total_alquileres
        if incluir_sanciones:
            total_general += total_sanciones
        total_general -= total_descuentos

        periodos.append(
            {
                "periodo": row.periodo,
                "total_alquileres": total_alquileres,
                "total_sanciones": total_sanciones,
                "total_descuentos": total_descuentos,
                "total_general": total_general,
            }
        )

        acumulados["total_alquileres"] += total_alquileres
        acumulados["total_sanciones"] += total_sanciones
        acumulados["total_descuentos"] += total_descuentos
        acumulados["total_general"] += total_general

    return {
        "periodos": periodos,
        "acumulado": acumulados,
        "incluir_sanciones": incluir_sanciones,
    }

from flask import Blueprint, jsonify, request

from entities import reportes
from db.connection import DatabaseEngineSingleton
from sqlalchemy.sql import text

reportes_bp = Blueprint("reportes", __name__, url_prefix="/api/reportes")


@reportes_bp.get("/alquileres")
def alquileres_detallados():
    try:
        dni = request.args.get("dni")
        fecha_desde = request.args.get("fecha_desde")
        fecha_hasta = request.args.get("fecha_hasta")

        data = reportes.get_alquileres_detallados(
            dni=dni,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
        )
        return jsonify(data), 200
    except Exception as exc:
        return (
            jsonify(
                {
                    "error": "No se pudieron obtener los alquileres",
                    "detalle": str(exc),
                }
            ),
            500,
        )


@reportes_bp.get("/vehiculos-mas-alquilados")
def vehiculos_mas_alquilados():
    try:
        fecha_desde = request.args.get("fecha_desde")
        fecha_hasta = request.args.get("fecha_hasta")
        limit = request.args.get("limit", type=int, default=10)

        data = reportes.get_vehiculos_mas_alquilados(
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            limit=limit,
        )
        return jsonify(data), 200
    except Exception as exc:
        return (
            jsonify(
                {
                    "error": "No se pudieron obtener los vehículos",
                    "detalle": str(exc),
                }
            ),
            500,
        )


@reportes_bp.get("/alquileres-por-periodo")
def alquileres_por_periodo():
    try:
        periodicidad = request.args.get("periodicidad", default="mes")
        fecha_desde = request.args.get("fecha_desde")
        fecha_hasta = request.args.get("fecha_hasta")

        data = reportes.get_alquileres_por_periodo(
            periodicidad=periodicidad,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
        )
        return jsonify(data), 200
    except Exception as exc:
        return (
            jsonify(
                {
                    "error": "No se pudieron obtener los alquileres por período",
                    "detalle": str(exc),
                }
            ),
            500,
        )


@reportes_bp.get("/facturacion-mensual")
def facturacion_mensual():
    try:
        fecha_desde = request.args.get("fecha_desde")
        fecha_hasta = request.args.get("fecha_hasta")
        incluir_sanciones = request.args.get(
            "incluir_sanciones", default="true"
        ).lower() in {"1", "true", "t", "yes", "y"}

        data = reportes.get_facturacion_mensual(
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            incluir_sanciones=incluir_sanciones,
        )
        return jsonify(data), 200
    except Exception as exc:
        return (
            jsonify(
                {
                    "error": "No se pudo obtener la facturación mensual",
                    "detalle": str(exc),
                }
            ),
            500,
        )

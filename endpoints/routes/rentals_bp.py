from flask import Blueprint, jsonify, request

from entities.registroAlquilerAuto import RegistroAlquilerAuto

rentals_bp = Blueprint("rentals", __name__, url_prefix="/api/rentals")


def _map_rental_row(row):
    cliente_nombre = " ".join(filter(None, [row.cliente_nombre, row.cliente_apellido])).strip()
    empleado_nombre = " ".join(filter(None, [row.empleado_nombre, row.empleado_apellido])).strip()
    auto_detalle = " ".join(filter(None, [row.auto_marca, row.auto_modelo, row.auto_patente])).strip()

    return {
        "id": row.id_alquiler,
        "cliente": cliente_nombre or str(row.dni_cliente or "N/A"),
        "auto": auto_detalle or str(row.patente_vehiculo or "No especificado"),
        "empleado": empleado_nombre or str(row.legajo_empleado or ""),
        "costo": float(row.precio) if row.precio is not None else 0,
        "fechaInicio": row.fecha_inicio or "",
        "fechaFin": row.fecha_fin or "",
        "sancion": "",
    }


@rentals_bp.route("/", methods=["GET"])
def list_rentals():
    rentals = RegistroAlquilerAuto.get_all_rentals_description()
    return jsonify(rentals), 200


@rentals_bp.route("/", methods=["POST"], strict_slashes=False)
def create_rental():
    payload = request.get_json() or {}

    required_fields = [
        "cliente",
        "auto",
        "empleado",
        "costo",
        "fechaInicio",
        "fechaFin",
    ]

    missing_fields = [field for field in required_fields if field not in payload or payload[field] in (None, "")]
    if missing_fields:
        return (
            jsonify(
                {
                    "error": "Faltan campos requeridos",
                    "campos": missing_fields,
                }
            ),
            400,
        )

    try:
        engine = DatabaseEngineSingleton().engine
        with engine.begin() as connection:
            insert_query = text(
                """
                INSERT INTO Alquileres_de_auto (
                    patente_vehiculo,
                    dni_cliente,
                    legajo_empleado,
                    precio,
                    fecha_inicio,
                    fecha_fin
                )
                VALUES (:patente, :dni_cliente, :legajo_empleado, :precio, :fecha_inicio, :fecha_fin)
                """
            )

            connection.execute(
                insert_query,
                {
                    "patente": payload["auto"],
                    "dni_cliente": payload["cliente"],
                    "legajo_empleado": payload["empleado"],
                    "precio": payload["costo"],
                    "fecha_inicio": payload["fechaInicio"],
                    "fecha_fin": payload["fechaFin"],
                },
            )

            created_id = connection.execute(text("SELECT last_insert_rowid() as id"))
            rental_id = created_id.scalar()

        return (
            jsonify(
                {
                    "message": "Alquiler creado exitosamente",
                    "id": rental_id,
                }
            ),
            201,
        )
    except Exception as exc:
        return (
            jsonify(
                {
                    "error": "No se pudo crear el alquiler",
                    "detalle": str(exc),
                }
            ),
            500,
        )

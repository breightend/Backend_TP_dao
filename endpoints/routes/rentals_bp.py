from flask import Blueprint, jsonify, request

from entities.registroAlquilerAuto import RegistroAlquilerAuto

rentals_bp = Blueprint("rentals", __name__, url_prefix="/api/rentals")

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
        rental = RegistroAlquilerAuto(
            fechaInicio=payload["fechaInicio"],
            fechaFin=payload["fechaFin"],
            precio=payload["costo"],
            dni_cliente=payload["cliente"],
            legajo_empleado=payload["empleado"],
            patente_vehiculo=payload["auto"],
        )
        rental.persist()
        return jsonify({"message": "Alquiler creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

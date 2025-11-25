from flask import Blueprint, jsonify, request

from entities.registroAlquilerAuto import RegistroAlquilerAuto

rentals_bp = Blueprint("rentals", __name__, url_prefix="/api/rentals")

@rentals_bp.route("/", methods=["GET"])
def list_rentals():
    rentals = RegistroAlquilerAuto.get_all_rentals_description()
    return jsonify(rentals), 200

@rentals_bp.route("/active", methods=["GET"])
def list_active_rentals():
    rentals = RegistroAlquilerAuto.get_active_rentals()
    return jsonify(rentals), 200

@rentals_bp.route("/carAvailable", methods=["GET"])
def car_available():
    patente_vehiculo = request.args.get("patente_vehiculo")
    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")

    if not patente_vehiculo or not fecha_inicio or not fecha_fin:
        return jsonify({"error": "Faltan campos requeridos"}), 400

    try:
        available = RegistroAlquilerAuto.car_available(patente_vehiculo, fecha_inicio, fecha_fin)
        return jsonify({"available": available}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@rentals_bp.route("/", methods=["POST"], strict_slashes=False)
def create_rental():
    payload = request.get_json() or {}

    required_fields = [
        "cliente",
        "auto",
        "empleado",
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
        from entities.auto import Auto
        from datetime import datetime

        auto = Auto.get_auto_by_patente(payload["auto"])
        if not auto:
            return jsonify({"error": "Auto no encontrado"}), 404

        fmt = "%Y-%m-%d"
        d1 = datetime.strptime(payload["fechaInicio"], fmt)
        d2 = datetime.strptime(payload["fechaFin"], fmt)
        days = (d2 - d1).days
        
        if days <= 0:
             return jsonify({"error": "La fecha de fin debe ser posterior a la fecha de inicio"}), 400

        precio_total = days * auto.costo

        fechaInicio = datetime.strptime(payload["fechaInicio"], fmt)
        hoy = datetime.now()

        if fechaInicio > hoy:
            id_estado = 11
        else:
            id_estado = 10


        rental = RegistroAlquilerAuto(
            fechaInicio=payload["fechaInicio"],
            fechaFin=payload["fechaFin"],
            precio=precio_total,
            dni_cliente=payload["cliente"],
            legajo_empleado=payload["empleado"],
            patente_vehiculo=payload["auto"],
            id_estado=id_estado
        )
        rental.persist()
        return jsonify({"message": "Alquiler creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@rentals_bp.route("/<int:id>", methods=["GET"])
def get_rental_by_id(id):
    try:
        rental = RegistroAlquilerAuto.get_rental_by_id(id, False)
        return jsonify(rental), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@rentals_bp.route("/<int:id>", methods=["PUT"])
def update_rental(id):

    payload = request.get_json() or {}

    nueva_fecha_fin = payload.get("fecha_fin")
    costo_extra = payload.get("costo_extra")

    if nueva_fecha_fin is None or costo_extra is None:
        return jsonify({"error": "Faltan campos requeridos"}), 400

    try:
        from entities.auto import Auto
        
        rental = RegistroAlquilerAuto.get_rental_by_id(id, True)
        if not rental:
             return jsonify({"error": "Alquiler no encontrado"}), 404
        
        auto = Auto.get_auto_by_patente(rental.patente_vehiculo)
        if not auto:
            return jsonify({"error": "Auto asociado al alquiler no encontrado"}), 404

        costo_diario_total = auto.costo + float(costo_extra)
             
        rental.actualizar_alquiler(nueva_fecha_fin, costo_diario_total)
        rental.persist()
        return jsonify({"message": "Alquiler actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@rentals_bp.route("/pay/<int:id>", methods=["PUT"])
def pay_rental(id):
    try:
        rental = RegistroAlquilerAuto.get_rental_by_id(id, True)
        if not rental:
             return jsonify({"error": "Alquiler no encontrado"}), 404
        rental.finalizarAlquiler()
        rental.persist()
        return jsonify({"message": "Alquiler finalizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


from flask import Blueprint, jsonify, request

from entities.auto import Auto

auto_bp = Blueprint("auto", __name__, url_prefix="/api")


@auto_bp.route("/autos", methods=["GET"])
def get_autos():
    try:
        autos_data = Auto.get_all_autos()
        return jsonify(autos_data), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener autos: {str(e)}"}), 500


@auto_bp.route("/autos/available", methods=["GET"])
def get_autos_available():
    try:
        autos_data = Auto.get_autos_available()

        autos_data = [auto.to_dict() for auto in autos_data]

        return jsonify(autos_data), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener autos: {str(e)}"}), 500

@auto_bp.route("/autos/availableForRental", methods=["GET"])
def get_autos_available_for_rental():
    try:
        fecha_inicio = request.args.get("fechaInicio")
        fecha_fin = request.args.get("fechaFin")

        autos_data = Auto.get_autos_available_for_rental(fecha_inicio, fecha_fin)

        autos_data = [auto.to_dict() for auto in autos_data]

        return jsonify(autos_data), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener autos: {str(e)}"}), 500

@auto_bp.route("/car/states", methods=["GET"])
def get_autos_states():
    try:
        autos_data = Auto.get_autos_states()
        return jsonify(autos_data), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener autos: {str(e)}"}), 500


@auto_bp.route("/autos/<string:patente>", methods=["GET"])
def get_auto_by_patente(patente):
    """
    Endpoint para obtener toda la información de un auto específico por patente
    Incluye: información básica, estado, seguro, historial de alquileres y mantenimientos
    """
    try:
        auto_data = Auto.get_auto_by_patente_with_details(patente)

        if auto_data is None:
            return jsonify(
                {"error": f"No se encontró un auto con patente: {patente}"}
            ), 404

        return jsonify(auto_data), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener auto: {str(e)}"}), 500


@auto_bp.route("/autos", methods=["POST"])
def create_auto():
    try:
        imagen_bytes = None

        if request.content_type and request.content_type.startswith(
            "multipart/form-data"
        ):
            marca = request.form.get("marca")
            modelo = request.form.get("modelo")
            anio = request.form.get("anio")
            color = request.form.get("color")
            costo = request.form.get("costo")
            patente = request.form.get("patente")
            periodicidadMantenimineto = request.form.get("periodicidadMantenimineto", 6)
            id_seguro = request.form.get("id_seguro")

            file = request.files.get("imagen")
            if file:
                imagen_bytes = file.read()
        else:
            datos_json = request.get_json() or {}
            marca = datos_json.get("marca")
            modelo = datos_json.get("modelo")
            anio = datos_json.get("anio")
            color = datos_json.get("color")
            costo = datos_json.get("costo")
            patente = datos_json.get("patente")
            periodicidadMantenimineto = datos_json.get("periodicidadMantenimineto", 6)
            id_seguro = datos_json.get("id_seguro")

            # aceptar imagen en base64 dentro del JSON opcionalmente
            imagen_b64 = datos_json.get("imagen")
            if imagen_b64:
                try:
                    import base64

                    imagen_bytes = base64.b64decode(imagen_b64)
                except Exception:
                    imagen_bytes = None

        if not all([marca, modelo, anio, color, costo, patente]):
            return (
                jsonify(
                    {
                        "error": "Faltan campos requeridos: marca, modelo, anio, color, costo, patente"
                    }
                ),
                400,
            )

        auto = Auto(
            marca=marca,
            modelo=modelo,
            anio=int(anio),
            color=color,
            costo=float(costo),
            patente=patente,
            periodicidadMantenimineto=int(periodicidadMantenimineto),
            imagen=imagen_bytes,
            id_seguro=id_seguro
        )

        auto.persist()

        return jsonify(
            {"message": "Auto creado exitosamente"}
        ), 201

    except ValueError as e:
        return jsonify({"error": f"Error en los tipos de datos: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Error al crear auto: {str(e)}"}), 500


@auto_bp.route("/autos/<string:patente>", methods=["PUT"])
def update_auto(patente):
    try:
        auto = Auto.get_auto_by_patente(patente)
        if not auto:
            return jsonify({"error": f"No se encontró un auto con patente: {patente}"}), 404

        costo = request.json.get("costo")
        estado = request.json.get("estado")
        periodicidadMantenimiento = request.json.get("periodicidad_mantenimiento")

        print(auto.to_dict())

        if costo is not None:
            auto.costo = costo
        if estado is not None:
            auto.id_estado = estado
        if periodicidadMantenimiento is not None:
            auto.periodicidadMantenimineto = periodicidadMantenimiento

        auto.persist()

        return jsonify({"message": "Auto actualizado exitosamente"})
    except Exception as e:
        return jsonify({"error": f"Error al actualizar auto: {str(e)}"}), 500


@auto_bp.route("/autos/<string:patente>", methods=["DELETE"])
def delete_auto(patente):
    try:
        auto = Auto.get_auto_by_patente(patente)
        if not auto:
            return jsonify({"error": f"No se encontró un auto con patente: {patente}"}), 404

        auto.delete()

        return jsonify({"message": "Auto eliminado exitosamente"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error al eliminar auto: {str(e)}"}), 500
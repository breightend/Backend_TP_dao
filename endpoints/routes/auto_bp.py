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


@auto_bp.route("/autos", methods=["POST"])
def create_auto():
    try:
        # Soportar tanto JSON como multipart/form-data con archivo 'imagen'
        imagen_bytes = None

        if request.content_type and request.content_type.startswith(
            "multipart/form-data"
        ):
            # campos vienen en request.form, el archivo en request.files['imagen']
            marca = request.form.get("marca")
            modelo = request.form.get("modelo")
            anio = request.form.get("anio")
            color = request.form.get("color")
            costo = request.form.get("costo")
            patente = request.form.get("patente")
            periodicidadMantenimineto = request.form.get("periodicidadMantenimineto", 6)

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
        )

        auto.persist()

        return jsonify(
            {"message": "Auto creado exitosamente", "auto": auto.to_dict()}
        ), 201

    except ValueError as e:
        return jsonify({"error": f"Error en los tipos de datos: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Error al crear auto: {str(e)}"}), 500

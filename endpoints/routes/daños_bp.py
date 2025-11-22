from flask import Blueprint, jsonify, request
from entities.tipoDaño import TipoDaño

daño_bp = Blueprint("daños", __name__, url_prefix="/api/daños")

@daño_bp.route("/tipoDaño/create", methods=["POST"])
def create_tipo_daño():
    try:
        data = request.get_json()
        nombre = data.get("nombre")
        costoBase = data.get("costoBase")

        if not nombre or not costoBase:
            return jsonify({"error": "Nombre and costoBase are required"}), 400

        tipo_daño = TipoDaño(nombre, costoBase)
        tipo_daño.persist()

        return jsonify({"message": "Tipo de daño creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@daño_bp.route("/tipoDaño", methods=["GET"])
def get_all_tipo_daños():
    try:
        tipo_daños = TipoDaño.get_all_tipo_daños()
        return jsonify(tipo_daños), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@daño_bp.route("/tipoDaño/<int:id>", methods=["GET"])
def get_tipo_daño_by_id(id):
    try:
        tipo_daño = TipoDaño.get_tipo_daño_by_id(int(id))
        if not tipo_daño:
            return jsonify({"error": "TipoDaño not found"}), 404
            
        return jsonify(tipo_daño), 200
    except ValueError:
        return jsonify({"error": "Invalid ID format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
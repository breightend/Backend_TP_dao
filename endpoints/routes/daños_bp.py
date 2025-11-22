from flask import Blueprint, jsonify, request
from entities.tipoDaño import TipoDaño
from entities.daño import Daño

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

@daño_bp.route("/create", methods=["POST"])
def create_daño():
    try:
        data = request.get_json()
        fecha = data.get("fecha")
        gravedad = data.get("gravedad")
        id_estado = data.get("id_estado")
        id_tipo_daño = data.get("id_tipo_daño")
        id_sancion = data.get("id_sancion")

        if not all([fecha, gravedad, id_estado, id_tipo_daño, id_sancion]):
             return jsonify({"error": "Missing required fields"}), 400

        daño = Daño(fecha, gravedad, id_estado, id_tipo_daño, id_sancion)
        daño.persist()

        return jsonify({"message": "Daño created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@daño_bp.route("/sancion/<int:id_sancion>", methods=["GET"])
def get_daños_by_sancion(id_sancion):
    try:
        daños = Daño.get_daños_by_sancion_id(id_sancion)
        return jsonify(daños), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
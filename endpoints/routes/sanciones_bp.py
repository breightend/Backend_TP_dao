from flask import Blueprint, jsonify, request
from entities.tipoSancion import TipoSancion
from entities.sancion import Sancion

sanciones_bp = Blueprint("sanciones", __name__, url_prefix="/api/sanciones")

@sanciones_bp.route("/tipoSanciones/create", methods=["POST"])
def create_tipo_sancion():
    try:
        data = request.get_json()
        descripcion = data.get("descripcion")
        
        if not descripcion:
            return jsonify({"error": "Descripcion is required"}), 400
            
        tipo_sancion = TipoSancion(descripcion)
        tipo_sancion.persist()
        
        return jsonify({"message": "Tipo de Sancion creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@sanciones_bp.route("/tipoSanciones", methods=["GET"])
def get_all_tipos_sancion():
    try:
        tipos_sancion = TipoSancion.get_all_tipos_sancion()
        return jsonify(tipos_sancion), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@sanciones_bp.route("/tipoSanciones/<int:id>", methods=["GET"])
def get_tipo_sancion_by_id(id):
    try:
        tipo_sancion = TipoSancion.get_tipo_sancion_by_id(id)
        return jsonify(tipo_sancion), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@sanciones_bp.route("/states", methods=["GET"])
def get_all_estados_sancion():
    try:
        estados = Sancion.get_all_estados_sanciones()
        return jsonify(estados), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

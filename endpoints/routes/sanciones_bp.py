from flask import Blueprint, jsonify, request
from entities.tipoSancion import TipoSancion
from entities.sancion import Sancion
from db.base import Base

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

@sanciones_bp.route("/create", methods=["POST"])
def create_sancion():
    try:
        data = request.get_json()
        fecha = data.get("fecha")
        id_tipo_sancion = data.get("id_tipo_sancion")
        id_estado = data.get("id_estado")
        costo_base = data.get("costo_base")
        descripcion = data.get("descripcion")
        id_alquiler = data.get("id_alquiler")

        if not all([fecha, id_tipo_sancion, id_estado, costo_base, descripcion, id_alquiler]):
             return jsonify({"error": "Missing required fields"}), 400

        tipo_sancion = TipoSancion.get_tipo_sancion_by_id(id_tipo_sancion)
        if not tipo_sancion:
            return jsonify({"error": "TipoSancion not found"}), 404

        # print("Tablas registradas en SQLAlchemy:", Base.metadata.tables.keys())

        sancion = Sancion(fecha, id_tipo_sancion, id_estado, costo_base, descripcion, id_alquiler)
        
        # print(sancion.to_dict())

        sancion.persist()

        return jsonify({"message": "Sancion created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@sanciones_bp.route("/alquiler/<int:id_alquiler>", methods=["GET"])
def get_sanciones_by_alquiler(id_alquiler):
    try:
        sanciones = Sancion.get_all_sanciones_of_alquiler(id_alquiler)
        return jsonify(sanciones), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

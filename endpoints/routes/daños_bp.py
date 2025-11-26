from flask import Blueprint, jsonify, request
from entities.tipoDaño import TipoDaño
from entities.daño import Daño
from datetime import datetime

daño_bp = Blueprint("danos", __name__, url_prefix="/api/danos")

@daño_bp.route("/tipoDano/create", methods=["POST"])
def create_tipo_dano():
    try:
        data = request.get_json()
        nombre = data.get("nombre")
        costoBase = data.get("costoBase")

        if not nombre or not costoBase:
            return jsonify({"error": "Nombre and costoBase are required"}), 400

        tipo_dano = TipoDaño(nombre, costoBase)
        tipo_dano.persist()

        return jsonify({"message": "Tipo de daño creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@daño_bp.route("/tipoDanos", methods=["GET"])
def get_all_tipo_danos():
    try:
        tipo_danos = TipoDaño.get_all_tipo_daños()
        return jsonify(tipo_danos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@daño_bp.route("/tipoDano/<int:id>", methods=["GET"])
def get_tipo_dano_by_id(id):
    try:
        tipo_dano = TipoDaño.get_tipo_daño_by_id(int(id))
        if not tipo_dano:
            return jsonify({"error": "TipoDano not found"}), 404
            
        return jsonify(tipo_dano), 200
    except ValueError:
        return jsonify({"error": "Invalid ID format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@daño_bp.route("/tipoDano/<int:id>", methods=["PUT"])
def update_tipo_dano(id):
    try:
        data = request.get_json()
        nombre = data.get("nombre")
        costoBase = data.get("costoBase")

        tipo_dano_data = TipoDaño.get_tipo_daño_by_id(int(id))
        if not tipo_dano_data:
            return jsonify({"error": "TipoDano not found"}), 404

        # Get the actual object to update
        from db.connection import DatabaseEngineSingleton
        from sqlalchemy.orm import sessionmaker
        engine = DatabaseEngineSingleton().engine
        Session = sessionmaker(bind=engine)
        session = Session()
        
        tipo_dano = session.query(TipoDaño).filter(TipoDaño.id == id).first()
        if tipo_dano:
            tipo_dano.update(nombre=nombre, costoBase=costoBase)
            session.close()
            return jsonify({"message": "Tipo de daño actualizado exitosamente"}), 200
        
        session.close()
        return jsonify({"error": "TipoDano not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@daño_bp.route("/tipoDano/<int:id>", methods=["DELETE"])
def delete_tipo_dano(id):
    try:
        deleted = TipoDaño.delete_tipo_daño(int(id))
        if deleted:
            return jsonify({"message": "Tipo de daño eliminado exitosamente"}), 200
        return jsonify({"error": "TipoDano not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@daño_bp.route("/create", methods=["POST"])
def create_dano():
    try:
        data = request.get_json()
        fecha = datetime.now().strftime("%Y-%m-%d")
        gravedad = int(data.get("gravedad")) 
        id_estado = 5
        id_tipo_dano = int(data.get("id_tipo_daño"))
        id_sancion = int(data.get("id_sancion"))

        if not all([fecha, gravedad, id_tipo_dano, id_sancion]):
             return jsonify({"error": "Missing required fields"}), 400

        dano = Daño(fecha, gravedad, id_estado, id_tipo_dano, id_sancion)
        dano.persist()

        return jsonify({"message": "Daño created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@daño_bp.route("/sancion/<int:id_sancion>", methods=["GET"])
def get_danos_by_sancion(id_sancion):
    try:
        danos = Daño.get_daños_by_sancion_id(id_sancion)
        return jsonify(danos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
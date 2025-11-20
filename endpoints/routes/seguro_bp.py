from flask import Blueprint, jsonify, request

from entities.tipoSeguro import TipoSeguro
from entities.seguro import Seguro
from db.connection import DatabaseEngineSingleton
from sqlalchemy.sql import text

seguro_bp = Blueprint("seguros", __name__, url_prefix="/api/seguros")

@seguro_bp.route("/", methods=["GET"])
def get_seguros():
    seguros = Seguro.get_all_seguros()
    return jsonify(seguros), 200

@seguro_bp.route("/tipoSeguros", methods=["GET"])
def get_tipo_seguros():
    tipos_seguros = TipoSeguro.get_all_tipo_seguro()
    return jsonify(tipos_seguros), 200

@seguro_bp.route("/createTipoSeguro", methods=["POST"])
def create_Tipo_seguro():
    try:
        datos = request.get_json()
    
        descripcion = datos.get("descripcion")
        
        nuevo_tipo_seguro = TipoSeguro(
            descripcion=descripcion,
        )

        nuevo_tipo_seguro.persist()
        return jsonify({"message": "Tipo de seguro creado exitosamente"}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(f"Error occurred while creating TipoSeguro: {e}")
        return jsonify({"error": "Error al crear el tipo de seguro"}), 500
    
@seguro_bp.route("/createSeguro", methods=["POST"])
def create_seguro():
    try:
        datos = request.get_json()

        print(datos)

        poliza = datos.get("poliza")
        compañia = datos.get("compañia")
        fechaVencimiento = datos.get("fechaVencimiento")
        tipoPoliza = datos.get("tipoPoliza")
        descripcion = datos.get("descripcion")
        costo = datos.get("costo")

        if(TipoSeguro.get_single_tipo_seguro(tipoPoliza) is None):
            raise ValueError("Tipo de seguro no existente")
        if(Seguro.get_single_seguro(poliza) is not None):
            raise ValueError("Seguro con esa poliza ya existente")
        
        nuevo_seguro = Seguro(
            poliza=poliza,
            compañia=compañia,
            fechaVencimiento=fechaVencimiento,
            tipoPoliza_id=tipoPoliza,
            descripcion=descripcion,
            costo=costo,
        )

        nuevo_seguro.persist()
        return jsonify({"message": "Seguro creado exitosamente"}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(f"Error occurred while creating Seguro: {e}")
        return jsonify({"error": "Error al crear el seguro"}), 500
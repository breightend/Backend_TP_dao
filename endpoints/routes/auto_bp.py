from flask import Blueprint, jsonify, request

from entities.auto import Auto

auto_bp = Blueprint("auto", __name__, url_prefix="/cars")

@auto_bp.route("/", methods=["GET"])
def get_autos():
  
  return jsonify({"WIP"}), 200
  

@auto_bp.route("/create", methods=["POST"])
def create_auto():
  
  datos_json = request.get_json()
  
  nombre = datos_json.get("nombre")
  modelo = datos_json.get("modelo")
  anio = datos_json.get("anio")
  color = datos_json.get("color")
  costo = datos_json.get("costo")
   
  return jsonify({"WIP"}), 201
from flask import Blueprint, jsonify, request

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route("/", methods=["GET"])
def get_users():
  return jsonify({"message": "List of users"}), 200
  

@users_bp.route("/create", methods=["POST"])
def create_users():
  datos_json = request.get_json()
  
  nombre = datos_json.get("nombre")
  apellido = datos_json.get("apellido")
  fechaNacimiento = datos_json.get("fechaNacimiento")
  dni = datos_json.get("DNI")
  email = datos_json.get("email")
  telefono = datos_json.get("telefono")
  
  
  
  return jsonify({"message": "WIP"}), 201
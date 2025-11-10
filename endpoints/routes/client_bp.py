from flask import Blueprint, jsonify, request
from entities.cliente import Cliente

client_bp = Blueprint('client', __name__, url_prefix='/clients')

@client_bp.route("/", methods=["GET"])
def get_users():
  return jsonify({"message": "List of users"}), 200
  

@client_bp.route("/create", methods=["POST"])
def create_users():
  datos_json = request.get_json()
  
  nombre = datos_json.get("nombre")
  apellido = datos_json.get("apellido")
  fechaNacimiento = datos_json.get("fechaNacimiento")
  dni = datos_json.get("DNI")
  email = datos_json.get("email")
  telefono = datos_json.get("telefono")
  direccion = datos_json.get("direccion")

  nuevo_cliente = Cliente(
      nombre=nombre,
      apellido=apellido,
      fechaNacimiento=fechaNacimiento,
      dni=dni,
      email=email,
      telefono=telefono,
      direccion=direccion
  )

  nuevo_cliente.persist()

  return jsonify({"message": "Cliente creado exitosamente"}), 201
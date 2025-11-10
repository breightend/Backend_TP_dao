from flask import Blueprint, jsonify, request
from entities.empleado import Empleado

empleado_bp = Blueprint('employe', __name__, url_prefix='/employees')

@empleado_bp.route("/", methods=["GET"])
def get_users():
  return jsonify({"message": "List of users"}), 200
  

@empleado_bp.route("/create", methods=["POST"])
def create_users():
  datos_json = request.get_json()
  
  nombre = datos_json.get("nombre")
  apellido = datos_json.get("apellido")
  fechaNacimiento = datos_json.get("fechaNacimiento")
  dni = datos_json.get("DNI")
  email = datos_json.get("email")
  telefono = datos_json.get("telefono")
  direccion = datos_json.get("direccion")
  legajo = datos_json.get("legajo")
  puesto = datos_json.get("puesto")
  salario = datos_json.get("salario")
  fechaInicioActividad = datos_json.get("fechaInicioActividad")

  nuevo_empleado = Empleado(
      nombre=nombre,
      apellido=apellido,
      direccion=direccion,
      fechaNacimiento=fechaNacimiento,
      dni=dni,
      email=email,
      telefono=telefono,
      legajo=legajo,
      puesto=puesto,
      salario=salario,
      fechaInicioActividad=fechaInicioActividad
  )

  nuevo_empleado.persist()

  return jsonify({"message": "Empleado creado exitosamente"}), 201
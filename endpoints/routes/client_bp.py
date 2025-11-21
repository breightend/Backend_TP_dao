from flask import Blueprint, jsonify, request

from entities.cliente import Cliente

client_bp = Blueprint("client", __name__, url_prefix="/clients")


@client_bp.route("/", methods=["GET"])
def get_users():
    clientes = Cliente.get_all_clients()

    return jsonify(clientes), 200

@client_bp.route("/specific", methods=["GET"])
def get_specific_user():

    dni = request.args.get("dni")

    cliente = Cliente.get_client_by_dni(dni)

    return jsonify(cliente), 200



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
        direccion=direccion,
    )

    print(nuevo_cliente.mostrar_informacion())

    nuevo_cliente.persist()

    return jsonify({"message": "Cliente creado exitosamente"}), 201


@client_bp.route("/editClient", methods=["PUT"])
def editClient():
    datos_json = request.get_json()

    dni = datos_json.get("dni")
    email = datos_json.get("email")
    telefono = datos_json.get("telefono")
    direccion = datos_json.get("direccion")

    cliente_existente = Cliente.get_client_by_dni(dni)
    if not cliente_existente:
        return jsonify({"message": "Cliente no encontrado"}), 404

    if email is not None:
        cliente_existente.email = email

    if telefono is not None:
        cliente_existente.telefono = telefono

    if direccion is not None:
        cliente_existente.direccion = direccion

    cliente_existente.persist()

    return jsonify({"message": "Cliente actualizado exitosamente"}), 200

from flask import Blueprint, jsonify, request

from entities.empleado import Empleado

empleado_bp = Blueprint("employe", __name__, url_prefix="/employees")


@empleado_bp.route("/", methods=["GET"])
def get_users():
    empleados = Empleado.get_all_employees()

    return jsonify(empleados), 200


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

    if Empleado.get_employee_by_dni(dni):
        return jsonify({"message": "Existe un empleado registrado con ese dni"}), 400

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
        fechaInicioActividad=fechaInicioActividad,
    )

    nuevo_empleado.persist()

    return jsonify({"message": "Empleado creado exitosamente"}), 201


@empleado_bp.route("/<legajo>", methods=["GET"])
def get_user(legajo):
    empleado = Empleado.get_employee_by_legajo(legajo)
    if not empleado:
        return jsonify({"message": "Empleado no encontrado"}), 404

    return jsonify(empleado.to_dict()), 200


@empleado_bp.route("/<dni>", methods=["PATCH"])
def update_user(dni):
    datos_json = request.get_json()

    email = datos_json.get("email")
    telefono = datos_json.get("telefono")
    direccion = datos_json.get("direccion")
    puesto = datos_json.get("puesto")
    salario = datos_json.get("salario")

    empleado = Empleado.get_employee_by_dni(dni)
    if not empleado:
        return jsonify({"message": "Empleado no encontrado"}), 404

    if email is not None:
        empleado.email = email
    if telefono is not None:
        empleado.telefono = telefono
    if direccion is not None:
        empleado.direccion = direccion
    if puesto is not None:
        empleado.puesto = puesto
    if salario is not None:
        empleado.salario = salario

    empleado.persist()

    return jsonify({"message": "Empleado actualizado exitosamente"}), 200


@empleado_bp.route("/<int:legajo>", methods=["DELETE"])
def delete_employee(legajo):
    try:
        empleado = Empleado.get_employee_by_legajo(legajo)
        if not empleado:
            return jsonify({"error": "Empleado no encontrado"}), 404

        empleado.delete()

        return jsonify({"message": "Empleado eliminado exitosamente"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error al eliminar empleado: {str(e)}"}), 500

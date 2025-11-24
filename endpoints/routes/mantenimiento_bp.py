from flask import Blueprint, jsonify, request
from entities.registroMantenimiento import RegistroMantenimiento
from entities.mantenimiento import Mantenimiento
from db.connection import DatabaseEngineSingleton
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

mantenimiento_bp = Blueprint("mantenimiento", __name__, url_prefix="/api/mantenimiento")

# ==================== ORDENES DE MANTENIMIENTO ====================

@mantenimiento_bp.route("/ordenes", methods=["GET"])
def get_ordenes():
    """Obtener todas las órdenes de mantenimiento con paginación y filtros"""
    try:
        # Parámetros de paginación
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 100, type=int)
        
        # Parámetros de filtro
        patente = request.args.get('patente', type=str)
        fecha_desde = request.args.get('fecha_desde', type=str)
        fecha_hasta = request.args.get('fecha_hasta', type=str)
        
        engine = DatabaseEngineSingleton().engine
        session_maker = sessionmaker(bind=engine)
        session = session_maker()
        
        # Construir query base
        query = session.query(RegistroMantenimiento)
        
        # Aplicar filtros
        if patente:
            query = query.filter(RegistroMantenimiento.patente_vehiculo.like(f'%{patente}%'))
        
        if fecha_desde:
            query = query.filter(RegistroMantenimiento.fecha_inicio >= fecha_desde)
        
        if fecha_hasta:
            query = query.filter(RegistroMantenimiento.fecha_fin <= fecha_hasta)
        
        # Contar total antes de paginar
        total = query.count()
        
        # Aplicar paginación
        ordenes = query.order_by(RegistroMantenimiento.id_orden.desc()).limit(per_page).offset((page - 1) * per_page).all()
        
        ordenes_data = [orden.to_dict() for orden in ordenes]
        
        session.close()
        
        return jsonify({
            "ordenes": ordenes_data,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page
        }), 200
        
    except Exception as e:
        print(f"Error al obtener órdenes: {e}")
        return jsonify({"error": "Error al obtener las órdenes de mantenimiento"}), 500


@mantenimiento_bp.route("/ordenes/<int:id_orden>", methods=["GET"])
def get_orden_by_id(id_orden):
    """Obtener una orden específica por ID"""
    try:
        orden_dict = RegistroMantenimiento.get_orden_by_id(id_orden)
        if orden_dict:
            return jsonify(orden_dict), 200
        return jsonify({"error": "Orden no encontrada"}), 404
    except Exception as e:
        print(f"Error al obtener orden {id_orden}: {e}")
        return jsonify({"error": "Error al obtener la orden"}), 500


@mantenimiento_bp.route("/ordenes", methods=["POST"])
def create_orden():
    """Crear una nueva orden de mantenimiento"""
    try:
        datos = request.get_json()
        
        # Validar campos requeridos
        required_fields = ["patente_vehiculo", "fecha_inicio", "fecha_fin"]
        missing_fields = [field for field in required_fields if field not in datos or not datos[field]]
        
        if missing_fields:
            return jsonify({
                "error": "Faltan campos requeridos",
                "campos": missing_fields
            }), 400
        
        # Validar que fecha_fin >= fecha_inicio
        from datetime import datetime
        try:
            fecha_inicio = datetime.strptime(datos["fecha_inicio"], "%Y-%m-%d")
            fecha_fin = datetime.strptime(datos["fecha_fin"], "%Y-%m-%d")
            
            if fecha_fin < fecha_inicio:
                return jsonify({
                    "error": "La fecha de fin debe ser mayor o igual a la fecha de inicio"
                }), 400
        except ValueError:
            return jsonify({
                "error": "Formato de fecha inválido. Use YYYY-MM-DD"
            }), 400
        
        # Crear la orden
        nueva_orden = RegistroMantenimiento(
            fecha_inicio=datos["fecha_inicio"],
            fecha_fin=datos["fecha_fin"],
            patente_vehiculo=datos["patente_vehiculo"]
        )
        
        # Si se incluye un primer mantenimiento
        if "primer_mantenimiento" in datos and datos["primer_mantenimiento"]:
            primer_mant = datos["primer_mantenimiento"]
            if "descripcion" in primer_mant and "precio" in primer_mant:
                mantenimiento = Mantenimiento(
                    descripcion=primer_mant["descripcion"],
                    precio=float(primer_mant["precio"])
                )
                nueva_orden.mantenimientos.append(mantenimiento)
        
        orden_id = nueva_orden.persist()
        
        return jsonify({
            "message": "Orden de mantenimiento creada exitosamente",
            "id_orden": orden_id
        }), 201
        
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(f"Error al crear orden: {e}")
        return jsonify({"error": "Error al crear la orden de mantenimiento"}), 500


@mantenimiento_bp.route("/ordenes/<int:id_orden>", methods=["DELETE"])
def delete_orden(id_orden):
    """Eliminar una orden de mantenimiento"""
    try:
        success = RegistroMantenimiento.delete_orden(id_orden)
        if success:
            return jsonify({"message": "Orden eliminada exitosamente"}), 200
        return jsonify({"error": "Orden no encontrada"}), 404
    except Exception as e:
        print(f"Error al eliminar orden {id_orden}: {e}")
        return jsonify({"error": "Error al eliminar la orden"}), 500


# ==================== MANTENIMIENTOS INDIVIDUALES ====================

@mantenimiento_bp.route("/ordenes/<int:id_orden>/mantenimientos", methods=["POST"])
def create_mantenimiento(id_orden):
    """Crear un nuevo mantenimiento para una orden específica"""
    try:
        # Verificar que la orden existe
        orden = RegistroMantenimiento.get_orden_by_id(id_orden)
        if not orden:
            return jsonify({"error": "Orden no encontrada"}), 404
        
        datos = request.get_json()
        
        # Validar campos requeridos
        if not datos.get("descripcion") or not datos.get("precio"):
            return jsonify({"error": "Descripción y precio son requeridos"}), 400
        
        # Crear el mantenimiento
        nuevo_mantenimiento = Mantenimiento(
            descripcion=datos["descripcion"],
            precio=float(datos["precio"]),
            id_orden_mantenimiento=id_orden
        )
        
        nuevo_mantenimiento.persist()
        
        return jsonify({
            "message": "Mantenimiento creado exitosamente",
            "id_mantenimiento": nuevo_mantenimiento.id_mantenimiento
        }), 201
        
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(f"Error al crear mantenimiento: {e}")
        return jsonify({"error": "Error al crear el mantenimiento"}), 500


@mantenimiento_bp.route("/mantenimientos/<int:id_mantenimiento>", methods=["PUT"])
def update_mantenimiento(id_mantenimiento):
    """Actualizar un mantenimiento existente"""
    try:
        datos = request.get_json()
        
        # Validar campos requeridos
        if not datos.get("descripcion") or not datos.get("precio"):
            return jsonify({"error": "Descripción y precio son requeridos"}), 400
        
        # Actualizar el mantenimiento
        mantenimiento = Mantenimiento.update_mantenimiento(
            id_mantenimiento=id_mantenimiento,
            descripcion=datos["descripcion"],
            precio=float(datos["precio"])
        )
        
        if mantenimiento:
            return jsonify({
                "message": "Mantenimiento actualizado exitosamente"
            }), 200
        
        return jsonify({"error": "Mantenimiento no encontrado"}), 404
        
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(f"Error al actualizar mantenimiento: {e}")
        return jsonify({"error": "Error al actualizar el mantenimiento"}), 500


@mantenimiento_bp.route("/mantenimientos/<int:id_mantenimiento>", methods=["DELETE"])
def delete_mantenimiento(id_mantenimiento):
    """Eliminar un mantenimiento"""
    try:
        success = Mantenimiento.delete_mantenimiento(id_mantenimiento)
        if success:
            return jsonify({"message": "Mantenimiento eliminado exitosamente"}), 200
        return jsonify({"error": "Mantenimiento no encontrado"}), 404
    except Exception as e:
        print(f"Error al eliminar mantenimiento: {e}")
        return jsonify({"error": "Error al eliminar el mantenimiento"}), 500


# ==================== ESTADÍSTICAS ====================

@mantenimiento_bp.route("/estadisticas", methods=["GET"])
def get_estadisticas():
    """Obtener estadísticas de mantenimiento"""
    try:
        engine = DatabaseEngineSingleton().engine
        session_maker = sessionmaker(bind=engine)
        session = session_maker()
        
        # Parámetros de filtro opcionales
        patente = request.args.get('patente', type=str)
        fecha_desde = request.args.get('fecha_desde', type=str)
        fecha_hasta = request.args.get('fecha_hasta', type=str)
        
        # Query base para órdenes
        query_ordenes = session.query(RegistroMantenimiento)
        
        # Aplicar filtros
        if patente:
            query_ordenes = query_ordenes.filter(RegistroMantenimiento.patente_vehiculo == patente)
        if fecha_desde:
            query_ordenes = query_ordenes.filter(RegistroMantenimiento.fecha_inicio >= fecha_desde)
        if fecha_hasta:
            query_ordenes = query_ordenes.filter(RegistroMantenimiento.fecha_fin <= fecha_hasta)
        
        # Total de órdenes
        total_ordenes = query_ordenes.count()
        
        # Total de mantenimientos y costo total
        query_mantenimientos = session.query(
            func.count(Mantenimiento.id_mantenimiento).label('total_mantenimientos'),
            func.sum(Mantenimiento.precio).label('costo_total'),
            func.avg(Mantenimiento.precio).label('costo_promedio')
        ).join(RegistroMantenimiento, Mantenimiento.id_orden_mantenimiento == RegistroMantenimiento.id_orden)
        
        # Aplicar mismos filtros a mantenimientos
        if patente:
            query_mantenimientos = query_mantenimientos.filter(RegistroMantenimiento.patente_vehiculo == patente)
        if fecha_desde:
            query_mantenimientos = query_mantenimientos.filter(RegistroMantenimiento.fecha_inicio >= fecha_desde)
        if fecha_hasta:
            query_mantenimientos = query_mantenimientos.filter(RegistroMantenimiento.fecha_fin <= fecha_hasta)
        
        stats = query_mantenimientos.first()
        stats_total_mantenimientos = stats.total_mantenimientos or 0 if stats else 0
        stats_costo_total = float(stats.costo_total) if stats and stats.costo_total else 0
        stats_costo_promedio = float(stats.costo_promedio) if stats and stats.costo_promedio else 0
        
        # Costo por vehículo (top 5)
        query_por_vehiculo = session.query(
            RegistroMantenimiento.patente_vehiculo,
            func.sum(Mantenimiento.precio).label('costo_total'),
            func.count(Mantenimiento.id_mantenimiento).label('cantidad_mantenimientos')
        ).join(Mantenimiento, RegistroMantenimiento.id_orden == Mantenimiento.id_orden_mantenimiento
        ).group_by(RegistroMantenimiento.patente_vehiculo
        ).order_by(func.sum(Mantenimiento.precio).desc()
        ).limit(5)
        
        # Aplicar filtros de fecha
        if fecha_desde:
            query_por_vehiculo = query_por_vehiculo.filter(RegistroMantenimiento.fecha_inicio >= fecha_desde)
        if fecha_hasta:
            query_por_vehiculo = query_por_vehiculo.filter(RegistroMantenimiento.fecha_fin <= fecha_hasta)
        
        top_vehiculos = query_por_vehiculo.all()
        
        session.close()
        
        return jsonify({
            "total_ordenes": total_ordenes,
            "total_mantenimientos": stats_total_mantenimientos,
            "costo_total": stats_costo_total,
            "costo_promedio": stats_costo_promedio,
            "top_vehiculos": [
                {
                    "patente": v.patente_vehiculo,
                    "costo_total": float(v.costo_total),
                    "cantidad_mantenimientos": v.cantidad_mantenimientos
                }
                for v in top_vehiculos
            ]
        }), 200
        
    except Exception as e:
        print(f"Error al obtener estadísticas: {e}")
        return jsonify({"error": "Error al obtener estadísticas"}), 500

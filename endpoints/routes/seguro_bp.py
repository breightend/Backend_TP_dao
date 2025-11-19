from flask import Blueprint, jsonify, request

from entities import tipoSeguro, seguro
from db.connection import DatabaseEngineSingleton
from sqlalchemy.sql import text

seguro_bp = Blueprint("seguros", __name__, url_prefix="/api/seguros")

@seguro_bp.route("/", methods=["GET"])
def get_seguros():
    seguros = seguro.Seguro.get_all_seguros()
    return jsonify(seguros), 200
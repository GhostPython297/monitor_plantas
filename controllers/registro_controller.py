"""Controller de registros — registro e histórico de cuidados."""

from flask import Blueprint

registro_bp = Blueprint("registro", __name__, url_prefix="/registros")


@registro_bp.route("/planta/<planta_id>/novo")
def novo(planta_id):
    """Exibe o formulário de registro de cuidado para uma planta. (a implementar)"""
    return f"Novo registro para planta {planta_id} — a implementar"


@registro_bp.route("/planta/<planta_id>")
def historico(planta_id):
    """Exibe o histórico de registros de uma planta. (a implementar)"""
    return f"Histórico da planta {planta_id} — a implementar"
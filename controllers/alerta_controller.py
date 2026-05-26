"""Controller de alertas — painel e ação rápida de rega."""

from flask import Blueprint

alerta_bp = Blueprint("alerta", __name__, url_prefix="/alertas")


@alerta_bp.route("/")
def painel():
    """Exibe o painel de alertas com plantas que precisam de cuidado. (a implementar)"""
    return "Painel de alertas — a implementar"


@alerta_bp.route("/rega-rapida/<planta_id>", methods=["POST"])
def rega_rapida(planta_id):
    """Registra rega rápida a partir do painel de alertas. (a implementar)"""
    return f"Rega rápida para planta {planta_id} — a implementar"
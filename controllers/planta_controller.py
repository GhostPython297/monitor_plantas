"""Controller de plantas — cadastro, listagem, detalhes e edição."""

from flask import Blueprint

planta_bp = Blueprint("planta", __name__, url_prefix="/plantas")


@planta_bp.route("/")
def listar():
    """Lista todas as plantas do colaborador autenticado. (a implementar)"""
    return "Listar plantas — a implementar"


@planta_bp.route("/nova")
def nova():
    """Exibe o formulário de cadastro de nova planta. (a implementar)"""
    return "Nova planta — a implementar"


@planta_bp.route("/<planta_id>")
def detalhes(planta_id):
    """Exibe os detalhes de uma planta específica. (a implementar)"""
    return f"Detalhes da planta {planta_id} — a implementar"


@planta_bp.route("/<planta_id>/editar")
def editar(planta_id):
    """Exibe o formulário de edição de uma planta. (a implementar)"""
    return f"Editar planta {planta_id} — a implementar"
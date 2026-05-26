"""Controller de colaboradores — autenticação e cadastro."""

from flask import Blueprint

colaborador_bp = Blueprint("colaborador", __name__, url_prefix="/colaborador")


@colaborador_bp.route("/login")
def login():
    """Exibe a página de login. (a implementar)"""
    return "Login — a implementar"


@colaborador_bp.route("/cadastro")
def cadastro():
    """Exibe o formulário de cadastro de colaborador. (a implementar)"""
    return "Cadastro — a implementar"


@colaborador_bp.route("/logout")
def logout():
    """Encerra a sessão do colaborador. (a implementar)"""
    return "Logout — a implementar"
"""Controller de colaboradores — autenticação e cadastro."""

from functools import wraps

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from models.usuario import Colaborador
from services.repositorio import (
    adicionar_colaborador,
    buscar_colaborador_por_email,
)

colaborador_bp = Blueprint("colaborador", __name__, url_prefix="/colaborador")


def login_required(f):
    """Decorator que exige sessão ativa; redireciona para login caso contrário."""

    @wraps(f)
    def decorated(*args, **kwargs):
        if "colaborador_id" not in session:
            return redirect(url_for("colaborador.login"))
        return f(*args, **kwargs)

    return decorated


@colaborador_bp.route("/login", methods=["GET", "POST"])
def login():
    """Autentica o colaborador e inicia a sessão Flask."""
    if "colaborador_id" in session:
        return redirect(url_for("planta.listar"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")
        colaborador = buscar_colaborador_por_email(email)

        if colaborador and colaborador.verificar_senha(senha):
            session["colaborador_id"] = colaborador.id
            session["colaborador_nome"] = colaborador.nome
            return redirect(url_for("planta.listar"))

        flash("E-mail ou senha incorretos.", "erro")

    return render_template("login.html")


@colaborador_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    """Cria um novo colaborador e inicia sessão automaticamente após o cadastro."""
    if "colaborador_id" in session:
        return redirect(url_for("planta.listar"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")

        if not nome or not email or not senha:
            flash("Todos os campos são obrigatórios.", "erro")
        elif buscar_colaborador_por_email(email):
            flash("Este e-mail já está cadastrado.", "erro")
        else:
            novo = Colaborador.criar(nome=nome, email=email, senha=senha)
            adicionar_colaborador(novo)
            session["colaborador_id"] = novo.id
            session["colaborador_nome"] = novo.nome
            return redirect(url_for("planta.listar"))

    return render_template("cadastro.html")


@colaborador_bp.route("/logout")
def logout():
    """Encerra a sessão do colaborador e redireciona para o login."""
    session.clear()
    return redirect(url_for("colaborador.login"))
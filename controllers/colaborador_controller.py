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
    atualizar_colaborador,
    buscar_colaborador_por_email,
    buscar_colaborador_por_id,
    remover_colaborador,
    remover_plantas_do_colaborador,
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
            atualizar_colaborador(colaborador)
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


@colaborador_bp.route("/perfil", methods=["GET", "POST"])
@login_required
def perfil():
    """Exibe e processa o formulário de edição do perfil do colaborador.

    Exige confirmação da senha atual antes de aplicar qualquer alteração.
    Permite atualizar nome, e-mail e senha separadamente ou em conjunto.
    """
    colaborador = buscar_colaborador_por_id(session["colaborador_id"])
    if not colaborador:
        session.clear()
        return redirect(url_for("colaborador.login"))

    if request.method == "POST":
        senha_atual = request.form.get("senha_atual", "")

        if not colaborador.verificar_senha(senha_atual):
            flash("Senha atual incorreta. Nenhuma alteração foi salva.", "erro")
            return render_template("perfil.html", colaborador=colaborador)

        novo_nome = request.form.get("nome", "").strip()
        novo_email = request.form.get("email", "").strip()
        nova_senha = request.form.get("nova_senha", "")

        if not novo_nome or not novo_email:
            flash("Nome e e-mail são obrigatórios.", "erro")
            return render_template("perfil.html", colaborador=colaborador)

        if novo_email != colaborador.email:
            conflito = buscar_colaborador_por_email(novo_email)
            if conflito and conflito.id != colaborador.id:
                flash("Este e-mail já está em uso por outro colaborador.", "erro")
                return render_template("perfil.html", colaborador=colaborador)

        colaborador.nome = novo_nome
        colaborador.email = novo_email

        if nova_senha:
            colaborador.set_senha(nova_senha)

        atualizar_colaborador(colaborador)
        session["colaborador_nome"] = colaborador.nome
        flash("Perfil atualizado com sucesso!", "sucesso")
        return redirect(url_for("colaborador.perfil"))

    return render_template("perfil.html", colaborador=colaborador)


@colaborador_bp.route("/excluir", methods=["GET", "POST"])
@login_required
def excluir():
    """Exibe a confirmação e processa a exclusão permanente da conta.

    Exige confirmação da senha atual. Remove o colaborador e todas as suas
    plantas antes de encerrar a sessão.
    """
    colaborador = buscar_colaborador_por_id(session["colaborador_id"])
    if not colaborador:
        session.clear()
        return redirect(url_for("colaborador.login"))

    if request.method == "POST":
        senha = request.form.get("senha", "")

        if not colaborador.verificar_senha(senha):
            flash("Senha incorreta. A conta não foi excluída.", "erro")
            return render_template("excluir_conta.html", colaborador=colaborador)

        qtd_plantas = remover_plantas_do_colaborador(colaborador.id)
        remover_colaborador(colaborador.id)
        session.clear()
        flash(
            f"Conta excluída. {qtd_plantas} planta(s) também foram removidas.",
            "sucesso",
        )
        return redirect(url_for("colaborador.login"))

    return render_template("excluir_conta.html", colaborador=colaborador)
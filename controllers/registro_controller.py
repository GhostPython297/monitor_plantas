"""Controller de registros — registro e histórico de cuidados."""

from datetime import date

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from controllers.colaborador_controller import login_required
from models.cuidado import Adubacao, Poda, Rega
from services.repositorio import atualizar_planta, buscar_planta_por_id

registro_bp = Blueprint("registro", __name__, url_prefix="/registros")

_TIPOS_CUIDADO = {
    Rega.tipo: Rega,
    Adubacao.tipo: Adubacao,
    Poda.tipo: Poda,
}


@registro_bp.route("/planta/<planta_id>/novo", methods=["GET", "POST"])
@login_required
def novo(planta_id):
    """Exibe e processa o formulário de registro de cuidado para uma planta."""
    planta = buscar_planta_por_id(planta_id)
    if not planta:
        flash("Planta não encontrada.", "erro")
        return redirect(url_for("planta.listar"))

    if planta.colaborador_id != session["colaborador_id"]:
        flash("Acesso negado.", "erro")
        return redirect(url_for("planta.listar"))

    if request.method == "POST":
        tipo = request.form.get("tipo", "rega")
        data_str = request.form.get("data", date.today().isoformat())
        observacao = request.form.get("observacao", "").strip()

        try:
            data_cuidado = date.fromisoformat(data_str)
            if data_cuidado > date.today():
                data_cuidado = date.today()
        except ValueError:
            data_cuidado = date.today()

        classe = _TIPOS_CUIDADO.get(tipo, Rega)
        cuidado = classe(data=data_cuidado, observacao=observacao)
        planta.registrar_cuidado(cuidado)
        atualizar_planta(planta)

        flash("Cuidado registrado com sucesso!", "sucesso")
        return redirect(url_for("planta.detalhes", planta_id=planta.id))

    return render_template(
        "novo_registro.html",
        planta=planta,
        hoje=date.today().isoformat(),
        tipos=list(_TIPOS_CUIDADO.keys()),
    )



"""Controller de alertas — painel e ação rápida de rega."""

from datetime import date

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    session,
    url_for,
)

from controllers.colaborador_controller import login_required
from models.alerta import Alerta
from models.cuidado import Rega
from services.repositorio import (
    atualizar_planta,
    buscar_planta_por_id,
    carregar_plantas_do_colaborador,
)

alerta_bp = Blueprint("alerta", __name__, url_prefix="/alertas")


@alerta_bp.route("/")
@login_required
def painel():
    """Exibe o painel com todas as plantas do colaborador que precisam de cuidado."""
    plantas = carregar_plantas_do_colaborador(session["colaborador_id"])
    alertas = [Alerta.from_planta(p) for p in plantas if p.precisa_cuidado()]
    return render_template("alertas.html", alertas=alertas)


@alerta_bp.route("/rega-rapida/<planta_id>", methods=["POST"])
@login_required
def rega_rapida(planta_id):
    """Registra uma rega com a data de hoje diretamente pelo painel de alertas."""
    planta = buscar_planta_por_id(planta_id)
    if not planta:
        flash("Planta não encontrada.", "erro")
        return redirect(url_for("alerta.painel"))

    if planta.colaborador_id != session["colaborador_id"]:
        flash("Acesso negado.", "erro")
        return redirect(url_for("alerta.painel"))

    rega = Rega(data=date.today(), observacao="Rega rápida via painel de alertas.")
    planta.registrar_cuidado(rega)
    atualizar_planta(planta)

    flash(f"Rega de '{planta.nome}' registrada com sucesso!", "sucesso")
    return redirect(url_for("alerta.painel"))
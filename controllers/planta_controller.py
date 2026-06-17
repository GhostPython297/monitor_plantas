"""Controller de plantas — cadastro, listagem, detalhes e edição."""

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
from models.planta import Planta
from services.especie_service import atualizar_especie_cache, buscar_especies, obter_especie
from services.repositorio import (
    adicionar_planta,
    atualizar_planta,
    buscar_planta_por_id,
    carregar_plantas_do_colaborador,
)

planta_bp = Blueprint("planta", __name__, url_prefix="/plantas")


@planta_bp.route("/")
@login_required
def listar():
    """Lista todas as plantas do colaborador autenticado."""
    plantas = carregar_plantas_do_colaborador(session["colaborador_id"])
    return render_template("plantas.html", plantas=plantas)


@planta_bp.route("/nova", methods=["GET", "POST"])
@login_required
def nova():
    """Exibe o formulário de cadastro de nova planta com busca de espécie.

    Fluxo de três etapas via campo ``acao``:
    - ``buscar``: consulta espécies pelo nome informado.
    - ``selecionar``: carrega os dados da espécie escolhida.
    - ``salvar``: persiste a nova planta.
    """
    if request.method == "POST":
        acao = request.form.get("acao", "")

        if acao == "buscar":
            query = request.form.get("query", "").strip()
            resultados = buscar_especies(query) if query else []
            return render_template("nova_planta.html", resultados=resultados, query=query)

        if acao == "selecionar":
            especie_id = request.form.get("especie_id", "")
            especie_selecionada = obter_especie(especie_id)
            return render_template("nova_planta.html", especie_selecionada=especie_selecionada)

        if acao == "salvar":
            nome = request.form.get("nome", "").strip()
            especie_id = request.form.get("especie_id", "")
            frequencia_raw = request.form.get("frequencia_rega", "7")

            if not nome:
                flash("O nome da planta é obrigatório.", "erro")
                return render_template("nova_planta.html")

            especie = obter_especie(especie_id) if especie_id else {}

            try:
                frequencia = int(frequencia_raw)
            except ValueError:
                frequencia = 7

            planta = Planta(
                nome=nome,
                especie=especie or {},
                frequencia_rega=frequencia,
                colaborador_id=session["colaborador_id"],
            )
            adicionar_planta(planta)
            flash("Planta cadastrada com sucesso!", "sucesso")
            return redirect(url_for("planta.listar"))

    return render_template("nova_planta.html")


@planta_bp.route("/<planta_id>")
@login_required
def detalhes(planta_id):
    """Exibe os detalhes e o histórico de cuidados de uma planta."""
    planta = buscar_planta_por_id(planta_id)
    if not planta:
        flash("Planta não encontrada.", "erro")
        return redirect(url_for("planta.listar"))

    if planta.colaborador_id != session["colaborador_id"]:
        flash("Acesso negado.", "erro")
        return redirect(url_for("planta.listar"))

    historico = sorted(planta.historico_cuidados, key=lambda c: c.data, reverse=True)
    return render_template("detalhe_planta.html", planta=planta, historico=historico)


@planta_bp.route("/<planta_id>/editar", methods=["GET", "POST"])
@login_required
def editar(planta_id):
    """Edita os dados de uma planta e registra as alterações no log."""
    planta = buscar_planta_por_id(planta_id)
    if not planta:
        flash("Planta não encontrada.", "erro")
        return redirect(url_for("planta.listar"))

    if planta.colaborador_id != session["colaborador_id"]:
        flash("Acesso negado.", "erro")
        return redirect(url_for("planta.listar"))

    if request.method == "POST":
        acao = request.form.get("acao", "salvar")

        if acao == "buscar_especie":
            query = request.form.get("query", "").strip()
            resultados = buscar_especies(query) if query else []
            return render_template("editar_planta.html", planta=planta, resultados=resultados, query=query)

        if acao == "selecionar_especie":
            especie_id = request.form.get("especie_id", "")
            especie_selecionada = obter_especie(especie_id)
            return render_template("editar_planta.html", planta=planta, especie_selecionada=especie_selecionada)

        novo_nome = request.form.get("nome", "").strip()
        frequencia_raw = request.form.get("frequencia_rega", "").strip()
        especie_id = request.form.get("especie_id", "")

        if not novo_nome:
            flash("O nome da planta é obrigatório.", "erro")
            return render_template("editar_planta.html", planta=planta)

        alteracoes = []

        if novo_nome != planta.nome:
            alteracoes.append(f"nome: '{planta.nome}' → '{novo_nome}'")
            planta.nome = novo_nome

        try:
            nova_freq = int(frequencia_raw)
            if nova_freq != planta.frequencia_rega:
                alteracoes.append(f"frequencia_rega: {planta.frequencia_rega} → {nova_freq}")
                planta.frequencia_rega = nova_freq
        except ValueError:
            pass

        if especie_id:
            nova_especie = obter_especie(especie_id)
            if nova_especie and nova_especie != planta.especie:
                alteracoes.append(
                    f"especie: '{planta.especie.get('nome_comum', '—')}' → '{nova_especie.get('nome_comum', '—')}'"
                )
                planta.especie = nova_especie

        if alteracoes:
            planta.log_edicoes.append({
                "data": date.today().isoformat(),
                "colaborador_id": session["colaborador_id"],
                "alteracoes": alteracoes,
            })

        atualizar_planta(planta)
        flash("Planta atualizada com sucesso!", "sucesso")
        return redirect(url_for("planta.detalhes", planta_id=planta.id))

    return render_template("editar_planta.html", planta=planta)


@planta_bp.route("/<planta_id>/atualizar_especie", methods=["POST"])
@login_required
def atualizar_especie(planta_id):
    """Force-refresh os dados da espécie da planta a partir da API."""
    planta = buscar_planta_por_id(planta_id)
    if not planta:
        flash("Planta não encontrada.", "erro")
        return redirect(url_for("planta.listar"))

    if planta.colaborador_id != session["colaborador_id"]:
        flash("Acesso negado.", "erro")
        return redirect(url_for("planta.listar"))

    especie_id = planta.especie.get("id") if planta.especie else None
    if not especie_id:
        flash("Esta planta não tem espécie vinculada.", "erro")
        return redirect(url_for("planta.editar", planta_id=planta_id))

    nova_especie = atualizar_especie_cache(especie_id)
    if nova_especie is None:
        flash("Não foi possível atualizar: espécie local ou API indisponível.", "erro")
        return redirect(url_for("planta.editar", planta_id=planta_id))

    planta.especie = nova_especie
    atualizar_planta(planta)
    flash("Dados da espécie atualizados com sucesso!", "sucesso")
    return redirect(url_for("planta.editar", planta_id=planta_id))
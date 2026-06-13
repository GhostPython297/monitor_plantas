"""Script de testes manuais do backend — Monitor de Plantas.

Executa uma sequência de operações cobrindo:
  - Criação e autenticação de colaborador
  - Cadastro e busca de plantas
  - Registro de cuidados (rega, adubação, poda)
  - Geração e verificação de alertas
  - Log de edições
  - Persistência JSON (salvar e recarregar)

Uso:
    python testar_backend.py
"""

import json
import os
import shutil
import sys
from datetime import date, timedelta

PASSOU = 0
FALHOU = 0


def ok(descricao: str) -> None:
    global PASSOU
    PASSOU += 1
    print(f"  [OK] {descricao}")


def falha(descricao: str, detalhe: str = "") -> None:
    global FALHOU
    FALHOU += 1
    print(f"  [FALHA] {descricao}", f"→ {detalhe}" if detalhe else "")


def secao(titulo: str) -> None:
    print(f"\n{'='*55}")
    print(f"  {titulo}")
    print(f"{'='*55}")


def _usar_dados_temporarios():
    """Redireciona a camada de persistência para arquivos temporários."""
    import services.repositorio as repo
    repo._ARQUIVO_COLABORADORES = "data/_test_colaboradores.json"
    repo._ARQUIVO_PLANTAS = "data/_test_plantas.json"
    for arq in [repo._ARQUIVO_COLABORADORES, repo._ARQUIVO_PLANTAS]:
        with open(arq, "w") as f:
            json.dump([], f)


def _limpar_dados_temporarios():
    import services.repositorio as repo
    for arq in [repo._ARQUIVO_COLABORADORES, repo._ARQUIVO_PLANTAS]:
        if os.path.exists(arq):
            os.remove(arq)


# ---------------------------------------------------------------------------
# 1. Models — Colaborador
# ---------------------------------------------------------------------------
secao("1. Model: Colaborador")

from models.usuario import Colaborador

colab = Colaborador.criar(nome="Ana Silva", email="ana@exemplo.com", senha="senha123")
ok("Colaborador criado") if colab.nome == "Ana Silva" else falha("Atributo nome")
ok("Senha hasheada") if colab.senha_hash != "senha123" else falha("Senha não foi hasheada")
ok("Verificação de senha correta") if colab.verificar_senha("senha123") else falha("Senha correta rejeitada")
ok("Verificação de senha errada") if not colab.verificar_senha("errada") else falha("Senha errada aceita")

d = colab.to_dict()
colab2 = Colaborador.from_dict(d)
ok("Serialização/deserialização JSON") if colab2.email == colab.email else falha("Email diverge após deserialização")

# ---------------------------------------------------------------------------
# 2. Models — Cuidado e hierarquia
# ---------------------------------------------------------------------------
secao("2. Model: Cuidado (Rega, Adubacao, Poda)")

from models.cuidado import Rega, Adubacao, Poda, Cuidado

hoje = date.today()

rega = Rega(data=hoje, observacao="Rega do dia")
ok("Rega criada com tipo correto") if rega.tipo == "rega" else falha("Tipo errado", rega.tipo)

adub = Adubacao(data=hoje)
ok("Adubação criada") if adub.tipo == "adubacao" else falha("Tipo errado", adub.tipo)

poda = Poda(data=hoje, observacao="Poda leve")
ok("Poda criada") if poda.tipo == "poda" else falha("Tipo errado", poda.tipo)

d_rega = rega.to_dict()
rega2 = Cuidado.from_dict(d_rega)
ok("from_dict retorna instância Rega") if isinstance(rega2, Rega) else falha("Tipo errado após from_dict", type(rega2))
ok("Data preservada") if rega2.data == hoje else falha("Data diverge")

# ---------------------------------------------------------------------------
# 3. Models — Planta
# ---------------------------------------------------------------------------
secao("3. Model: Planta")

from models.planta import Planta

especie_teste = {
    "id": "local-1",
    "nome_comum": "Samambaia",
    "nome_cientifico": "Nephrolepis exaltata",
    "frequencia_rega": 3,
}

planta = Planta(
    nome="Minha Samambaia",
    especie=especie_teste,
    frequencia_rega=3,
    colaborador_id=colab.id,
)

ok("Planta criada") if planta.nome == "Minha Samambaia" else falha("Nome diverge")
ok("dias_sem_cuidado() → None sem histórico") if planta.dias_sem_cuidado() is None else falha("Esperado None")
ok("precisa_cuidado() → True sem histórico") if planta.precisa_cuidado() else falha("Deveria precisar de cuidado")

rega_ontem = Rega(data=hoje - timedelta(days=1))
planta.registrar_cuidado(rega_ontem)
ok("Cuidado registrado") if len(planta.historico_cuidados) == 1 else falha("Histórico não atualizado")
ok("dias_sem_cuidado() → 1") if planta.dias_sem_cuidado() == 1 else falha("Dias incorretos", planta.dias_sem_cuidado())
ok("precisa_cuidado() → False (1 dia, freq=3)") if not planta.precisa_cuidado() else falha("Não deveria precisar ainda")

rega_antiga = Rega(data=hoje - timedelta(days=5))
planta.registrar_cuidado(rega_antiga)
ok("precisa_cuidado() considera a data mais recente") if not planta.precisa_cuidado() else falha("Deveria usar data mais recente")

planta2 = Planta(
    nome="Cacto Velho",
    especie={},
    frequencia_rega=7,
    colaborador_id=colab.id,
)
rega_atrasada = Rega(data=hoje - timedelta(days=10))
planta2.registrar_cuidado(rega_atrasada)
ok("precisa_cuidado() → True (10 dias, freq=7)") if planta2.precisa_cuidado() else falha("Deveria precisar de cuidado")

d_planta = planta.to_dict()
planta_rec = Planta.from_dict(d_planta)
ok("Serialização/deserialização Planta") if planta_rec.nome == planta.nome else falha("Nome diverge")
ok("Histórico preservado") if len(planta_rec.historico_cuidados) == 2 else falha("Histórico perdido", len(planta_rec.historico_cuidados))

# ---------------------------------------------------------------------------
# 4. Models — Alerta
# ---------------------------------------------------------------------------
secao("4. Model: Alerta")

from models.alerta import Alerta

alerta = Alerta.from_planta(planta2)
ok("Alerta criado a partir de planta") if alerta.planta_id == planta2.id else falha("ID diverge")
ok("dias_sem_cuidado correto") if alerta.dias_sem_cuidado == 10 else falha("Dias incorretos", alerta.dias_sem_cuidado)
ok("dias_atraso correto") if alerta.dias_atraso == 3 else falha("Atraso incorreto", alerta.dias_atraso)

alerta_sem_hist = Alerta.from_planta(
    Planta(nome="Planta Nova", especie={}, frequencia_rega=5, colaborador_id=colab.id)
)
ok("Alerta sem histórico: dias_sem_cuidado → None") if alerta_sem_hist.dias_sem_cuidado is None else falha("Esperado None")
ok("Alerta sem histórico: dias_atraso → None") if alerta_sem_hist.dias_atraso is None else falha("Esperado None")

# ---------------------------------------------------------------------------
# 5. Services — Repositório JSON
# ---------------------------------------------------------------------------
secao("5. Service: Repositório (persistência JSON)")

_usar_dados_temporarios()

from services.repositorio import (
    adicionar_colaborador,
    buscar_colaborador_por_email,
    buscar_colaborador_por_id,
    adicionar_planta,
    buscar_planta_por_id,
    carregar_plantas_do_colaborador,
    atualizar_planta,
    carregar_colaboradores,
    carregar_plantas,
)

adicionar_colaborador(colab)
ok("Colaborador persistido")

c_buscado = buscar_colaborador_por_email("ana@exemplo.com")
ok("buscar_colaborador_por_email") if c_buscado and c_buscado.nome == "Ana Silva" else falha("Não encontrado")

c_por_id = buscar_colaborador_por_id(colab.id)
ok("buscar_colaborador_por_id") if c_por_id and c_por_id.id == colab.id else falha("Não encontrado por ID")

nao_existe = buscar_colaborador_por_email("nao@existe.com")
ok("Email inexistente retorna None") if nao_existe is None else falha("Deveria ser None")

adicionar_planta(planta)
adicionar_planta(planta2)
ok("Plantas persistidas")

plantas_carregadas = carregar_plantas()
ok("Plantas carregadas do JSON") if len(plantas_carregadas) == 2 else falha("Quantidade incorreta", len(plantas_carregadas))

plantas_colab = carregar_plantas_do_colaborador(colab.id)
ok("Filtro por colaborador") if len(plantas_colab) == 2 else falha("Filtro incorreto", len(plantas_colab))

p_buscada = buscar_planta_por_id(planta.id)
ok("buscar_planta_por_id") if p_buscada and p_buscada.nome == planta.nome else falha("Não encontrada")

planta.nome = "Samambaia Editada"
planta.log_edicoes.append({
    "data": hoje.isoformat(),
    "colaborador_id": colab.id,
    "alteracoes": ["nome: 'Minha Samambaia' → 'Samambaia Editada'"],
})
resultado = atualizar_planta(planta)
ok("atualizar_planta retorna True") if resultado else falha("Retornou False")

p_atualizada = buscar_planta_por_id(planta.id)
ok("Edição persistida") if p_atualizada.nome == "Samambaia Editada" else falha("Nome não atualizado")
ok("Log de edições persistido") if len(p_atualizada.log_edicoes) == 1 else falha("Log não salvo")

falso_id = atualizar_planta(
    Planta(nome="X", especie={}, frequencia_rega=1, colaborador_id=colab.id, id="id-inexistente")
)
ok("atualizar_planta retorna False para ID inexistente") if not falso_id else falha("Deveria ser False")

# ---------------------------------------------------------------------------
# 6. Services — Espécie (fallback)
# ---------------------------------------------------------------------------
secao("6. Service: EspecieService (fallback local)")

from services.especie_service import buscar_especies, obter_especie

resultados = buscar_especies("samambaia")
ok("buscar_especies retorna resultados") if resultados else falha("Nenhum resultado")
ok("Resultado contém nome_comum") if "nome_comum" in resultados[0] else falha("Chave nome_comum ausente")
ok("Resultado contém frequencia_rega") if "frequencia_rega" in resultados[0] else falha("Chave frequencia_rega ausente")

especie = obter_especie("local-1")
ok("obter_especie por ID local") if especie and especie["nome_comum"] == "Samambaia" else falha("Espécie não encontrada")

especie_invalida = obter_especie("local-99")
ok("ID inexistente retorna None") if especie_invalida is None else falha("Deveria ser None")

resultados_vazio = buscar_especies("")
ok("Busca vazia retorna catálogo completo") if resultados_vazio else falha("Lista vazia inesperada")

# ---------------------------------------------------------------------------
# 7. Fluxo integrado — da criação ao alerta
# ---------------------------------------------------------------------------
secao("7. Fluxo integrado: cadastro → cuidado → alerta")

from services.repositorio import carregar_plantas_do_colaborador as _carregar

colab_b = Colaborador.criar(nome="Bruno Lima", email="bruno@exemplo.com", senha="abc123")
adicionar_colaborador(colab_b)

planta_b = Planta(
    nome="Orquídea do Bruno",
    especie={"id": "local-4", "nome_comum": "Orquídea", "nome_cientifico": "Phalaenopsis sp.", "frequencia_rega": 7},
    frequencia_rega=7,
    colaborador_id=colab_b.id,
)
adicionar_planta(planta_b)
ok("Segundo colaborador e planta persistidos")

plantas_b = _carregar(colab_b.id)
ok("Isolamento por colaborador") if len(plantas_b) == 1 and plantas_b[0].id == planta_b.id else falha("Isolamento falhou")

p = buscar_planta_por_id(planta_b.id)
ok("Orquídea precisa de cuidado (sem histórico)") if p.precisa_cuidado() else falha("Deveria precisar")

rega_hoje = Rega(data=hoje, observacao="Rega inicial")
p.registrar_cuidado(rega_hoje)
atualizar_planta(p)

p_apos = buscar_planta_por_id(planta_b.id)
ok("Após rega, não precisa de cuidado") if not p_apos.precisa_cuidado() else falha("Ainda deveria estar ok")

alertas_b = [Alerta.from_planta(pl) for pl in _carregar(colab_b.id) if pl.precisa_cuidado()]
ok("Painel de alertas vazio após rega") if len(alertas_b) == 0 else falha("Alerta indevido", len(alertas_b))

# ---------------------------------------------------------------------------
# Resultado final
# ---------------------------------------------------------------------------
_limpar_dados_temporarios()

print(f"\n{'='*55}")
total = PASSOU + FALHOU
print(f"  Resultado: {PASSOU}/{total} testes passaram", end="")
if FALHOU:
    print(f"  ({FALHOU} FALHA(S))")
    sys.exit(1)
else:
    print("  — Tudo OK!")

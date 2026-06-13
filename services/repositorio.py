"""Módulo de persistência JSON para colaboradores e plantas."""

import json
import os
from typing import List

from models.usuario import Colaborador
from models.planta import Planta

_BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
_ARQUIVO_COLABORADORES = os.path.join(_BASE_DIR, "colaboradores.json")
_ARQUIVO_PLANTAS = os.path.join(_BASE_DIR, "plantas.json")


def _garantir_diretorio() -> None:
    """Cria o diretório de dados caso ele não exista."""
    os.makedirs(_BASE_DIR, exist_ok=True)


def _ler_json(caminho: str) -> list:
    """Lê e retorna o conteúdo de um arquivo JSON como lista.

    Retorna lista vazia se o arquivo não existir ou estiver corrompido.

    Args:
        caminho: Caminho absoluto para o arquivo JSON.

    Returns:
        Lista de dicionários lida do arquivo, ou lista vazia em caso de falha.
    """
    if not os.path.exists(caminho):
        return []
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def _escrever_json(caminho: str, dados: list) -> None:
    """Serializa e grava uma lista de dicionários em um arquivo JSON.

    Args:
        caminho: Caminho absoluto para o arquivo JSON.
        dados: Lista de dicionários a ser persistida.
    """
    _garantir_diretorio()
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def carregar_colaboradores() -> List[Colaborador]:
    """Carrega todos os colaboradores persistidos no arquivo JSON.

    Returns:
        Lista de instâncias de :class:`Colaborador`.
    """
    registros = _ler_json(_ARQUIVO_COLABORADORES)
    return [Colaborador.from_dict(r) for r in registros]


def salvar_colaboradores(colaboradores: List[Colaborador]) -> None:
    """Persiste a lista completa de colaboradores no arquivo JSON.

    Substitui integralmente o conteúdo anterior do arquivo.

    Args:
        colaboradores: Lista de instâncias de :class:`Colaborador` a salvar.
    """
    _escrever_json(_ARQUIVO_COLABORADORES, [c.to_dict() for c in colaboradores])


def buscar_colaborador_por_email(email: str):
    """Retorna o colaborador com o e-mail informado, ou None se não encontrado.

    Args:
        email: Endereço de e-mail a buscar.

    Returns:
        Instância de :class:`Colaborador` ou None.
    """
    for colaborador in carregar_colaboradores():
        if colaborador.email == email:
            return colaborador
    return None


def buscar_colaborador_por_id(id: str):
    """Retorna o colaborador com o id informado, ou None se não encontrado.

    Args:
        id: Identificador único do colaborador.

    Returns:
        Instância de :class:`Colaborador` ou None.
    """
    for colaborador in carregar_colaboradores():
        if colaborador.id == id:
            return colaborador
    return None


def adicionar_colaborador(colaborador: Colaborador) -> None:
    """Adiciona um novo colaborador à lista persistida.

    Args:
        colaborador: Instância de :class:`Colaborador` a adicionar.
    """
    colaboradores = carregar_colaboradores()
    colaboradores.append(colaborador)
    salvar_colaboradores(colaboradores)


def carregar_plantas() -> List[Planta]:
    """Carrega todas as plantas persistidas no arquivo JSON.

    Returns:
        Lista de instâncias de :class:`Planta`.
    """
    registros = _ler_json(_ARQUIVO_PLANTAS)
    return [Planta.from_dict(r) for r in registros]


def salvar_plantas(plantas: List[Planta]) -> None:
    """Persiste a lista completa de plantas no arquivo JSON.

    Substitui integralmente o conteúdo anterior do arquivo.

    Args:
        plantas: Lista de instâncias de :class:`Planta` a salvar.
    """
    _escrever_json(_ARQUIVO_PLANTAS, [p.to_dict() for p in plantas])


def carregar_plantas_do_colaborador(colaborador_id: str) -> List[Planta]:
    """Retorna apenas as plantas pertencentes ao colaborador informado.

    Args:
        colaborador_id: ID do colaborador dono das plantas.

    Returns:
        Lista de instâncias de :class:`Planta` do colaborador.
    """
    return [p for p in carregar_plantas() if p.colaborador_id == colaborador_id]


def buscar_planta_por_id(id: str):
    """Retorna a planta com o id informado, ou None se não encontrada.

    Args:
        id: Identificador único da planta.

    Returns:
        Instância de :class:`Planta` ou None.
    """
    for planta in carregar_plantas():
        if planta.id == id:
            return planta
    return None


def adicionar_planta(planta: Planta) -> None:
    """Adiciona uma nova planta à lista persistida.

    Args:
        planta: Instância de :class:`Planta` a adicionar.
    """
    plantas = carregar_plantas()
    plantas.append(planta)
    salvar_plantas(plantas)


def atualizar_planta(planta_atualizada: Planta) -> bool:
    """Substitui os dados de uma planta existente na lista persistida.

    Localiza a planta pelo id e substitui o registro inteiro.

    Args:
        planta_atualizada: Instância de :class:`Planta` com os dados novos.

    Returns:
        True se a planta foi encontrada e atualizada, False caso contrário.
    """
    plantas = carregar_plantas()
    for i, planta in enumerate(plantas):
        if planta.id == planta_atualizada.id:
            plantas[i] = planta_atualizada
            salvar_plantas(plantas)
            return True
    return False

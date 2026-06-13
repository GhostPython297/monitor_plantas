"""Módulo de integração com a API externa de espécies de plantas (Perenual)."""

import os
from typing import List, Optional

import requests

_BASE_URL = "https://perenual.com/api"
_API_KEY = os.environ.get("PERENUAL_API_KEY", "")

_MAPA_FREQUENCIA_REGA = {
    "frequent": 2,
    "average": 5,
    "minimum": 10,
    "none": 30,
}

_FALLBACK_ESPECIES = [
    {
        "id": "local-1",
        "nome_comum": "Samambaia",
        "nome_cientifico": "Nephrolepis exaltata",
        "frequencia_rega": 3,
        "luz": "Luz indireta",
        "temp_minima": 10,
    },
    {
        "id": "local-2",
        "nome_comum": "Suculenta",
        "nome_cientifico": "Echeveria sp.",
        "frequencia_rega": 14,
        "luz": "Pleno sol",
        "temp_minima": 5,
    },
    {
        "id": "local-3",
        "nome_comum": "Espada-de-São-Jorge",
        "nome_cientifico": "Dracaena trifasciata",
        "frequencia_rega": 10,
        "luz": "Luz indireta",
        "temp_minima": 10,
    },
    {
        "id": "local-4",
        "nome_comum": "Orquídea",
        "nome_cientifico": "Phalaenopsis sp.",
        "frequencia_rega": 7,
        "luz": "Luz indireta",
        "temp_minima": 15,
    },
    {
        "id": "local-5",
        "nome_comum": "Cacto",
        "nome_cientifico": "Cactaceae sp.",
        "frequencia_rega": 21,
        "luz": "Pleno sol",
        "temp_minima": 5,
    },
]


def _frequencia_em_dias(watering: str) -> int:
    """Converte o campo textual de rega da API para um intervalo em dias.

    Args:
        watering: Valor textual da API (ex: ``"Frequent"``, ``"Average"``).

    Returns:
        Número de dias sugerido para o intervalo de rega.
    """
    return _MAPA_FREQUENCIA_REGA.get(watering.lower(), 7)


def _normalizar_especie(item: dict) -> dict:
    """Converte um item da resposta da API Perenual para o formato interno.

    Args:
        item: Dicionário retornado pela API Perenual.

    Returns:
        Dicionário padronizado com as chaves usadas pela aplicação.
    """
    nomes_cientificos = item.get("scientific_name", [])
    nome_cientifico = nomes_cientificos[0] if nomes_cientificos else ""

    sunlight = item.get("sunlight", [])
    if isinstance(sunlight, list):
        luz = ", ".join(sunlight)
    else:
        luz = str(sunlight)

    hardiness = item.get("hardiness", {}) or {}
    temp_minima_raw = hardiness.get("min", "0")
    try:
        temp_minima = int(str(temp_minima_raw).replace("°", "").strip())
    except (ValueError, TypeError):
        temp_minima = 0

    return {
        "id": str(item.get("id", "")),
        "nome_comum": item.get("common_name", nome_cientifico),
        "nome_cientifico": nome_cientifico,
        "frequencia_rega": _frequencia_em_dias(item.get("watering", "average")),
        "luz": luz,
        "temp_minima": temp_minima,
    }


def _api_disponivel() -> bool:
    """Verifica se a chave de API está configurada.

    Returns:
        True se a variável de ambiente ``PERENUAL_API_KEY`` estiver definida.
    """
    return bool(_API_KEY)


def buscar_especies(query: str) -> List[dict]:
    """Busca espécies de plantas pelo nome informado.

    Consulta a API Perenual quando a chave estiver disponível. Em caso de
    ausência da chave ou falha na requisição, retorna o catálogo local de
    fallback filtrado pelo termo buscado.

    Args:
        query: Termo de busca (nome comum ou científico da espécie).

    Returns:
        Lista de dicionários com as chaves ``id``, ``nome_comum``,
        ``nome_cientifico``, ``frequencia_rega``, ``luz`` e ``temp_minima``.
    """
    if not _api_disponivel():
        return _buscar_fallback(query)

    try:
        resposta = requests.get(
            f"{_BASE_URL}/species-list",
            params={"key": _API_KEY, "q": query},
            timeout=5,
        )
        resposta.raise_for_status()
        dados = resposta.json()
        return [_normalizar_especie(item) for item in dados.get("data", [])]
    except requests.RequestException:
        return _buscar_fallback(query)


def obter_especie(id: str) -> Optional[dict]:
    """Retorna os detalhes completos de uma espécie pelo seu identificador.

    Consulta a API Perenual quando a chave estiver disponível. Em caso de
    ausência da chave, falha na requisição ou ID local (prefixo ``local-``),
    tenta localizar a espécie no catálogo de fallback.

    Args:
        id: Identificador da espécie (numérico da API ou ``local-N`` do fallback).

    Returns:
        Dicionário com os dados da espécie, ou None se não encontrada.
    """
    if str(id).startswith("local-"):
        return _buscar_fallback_por_id(id)

    if not _api_disponivel():
        return _buscar_fallback_por_id(id)

    try:
        resposta = requests.get(
            f"{_BASE_URL}/species/details/{id}",
            params={"key": _API_KEY},
            timeout=5,
        )
        resposta.raise_for_status()
        return _normalizar_especie(resposta.json())
    except requests.RequestException:
        return _buscar_fallback_por_id(id)


def _buscar_fallback(query: str) -> List[dict]:
    """Filtra o catálogo local pelo termo de busca (case-insensitive).

    Args:
        query: Termo de busca.

    Returns:
        Lista de espécies do catálogo local que correspondem ao termo.
    """
    termo = query.lower()
    return [
        esp
        for esp in _FALLBACK_ESPECIES
        if termo in esp["nome_comum"].lower() or termo in esp["nome_cientifico"].lower()
    ] or _FALLBACK_ESPECIES


def _buscar_fallback_por_id(id: str) -> Optional[dict]:
    """Localiza uma espécie no catálogo local pelo identificador.

    Args:
        id: Identificador da espécie no catálogo local (ex: ``local-1``).

    Returns:
        Dicionário com os dados da espécie, ou None se não encontrada.
    """
    for esp in _FALLBACK_ESPECIES:
        if esp["id"] == str(id):
            return esp
    return None

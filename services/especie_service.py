"""Módulo de integração com a API externa de espécies de plantas (Perenual).

Utiliza um cache em JSON (data/especies_cache.json) para minimizar chamadas à
API gratuita. Consulta o cache antes de qualquer requisição e persiste os
resultados obtidos para uso futuro.
"""

import json
import os
import unicodedata
from typing import List, Optional

import requests

_BASE_URL = "https://perenual.com/api"
_API_KEY = os.environ.get("PERENUAL_API_KEY", "")

_CACHE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "especies_cache.json")

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
        "imagem": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Nephrolepis_exaltata_2.jpg/320px-Nephrolepis_exaltata_2.jpg",
    },
    {
        "id": "local-2",
        "nome_comum": "Suculenta",
        "nome_cientifico": "Echeveria sp.",
        "frequencia_rega": 14,
        "luz": "Pleno sol",
        "temp_minima": 5,
        "imagem": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Echeveria_elegans_2.jpg/320px-Echeveria_elegans_2.jpg",
    },
    {
        "id": "local-3",
        "nome_comum": "Espada-de-São-Jorge",
        "nome_cientifico": "Dracaena trifasciata",
        "frequencia_rega": 10,
        "luz": "Luz indireta",
        "temp_minima": 10,
        "imagem": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Sansevieria_trifasciata_Prain.jpg/320px-Sansevieria_trifasciata_Prain.jpg",
    },
    {
        "id": "local-4",
        "nome_comum": "Orquídea",
        "nome_cientifico": "Phalaenopsis sp.",
        "frequencia_rega": 7,
        "luz": "Luz indireta",
        "temp_minima": 15,
        "imagem": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Phalaenopsis_RWTH_01.jpg/320px-Phalaenopsis_RWTH_01.jpg",
    },
    {
        "id": "local-5",
        "nome_comum": "Cacto",
        "nome_cientifico": "Cactaceae sp.",
        "frequencia_rega": 21,
        "luz": "Pleno sol",
        "temp_minima": 5,
        "imagem": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Cleistocactus_strausii_ies.jpg/320px-Cleistocactus_strausii_ies.jpg",
    },
]


# ---------------------------------------------------------------------------
# Cache helpers
# ---------------------------------------------------------------------------

def _carregar_cache() -> dict:
    """Carrega o cache do disco. Retorna estrutura vazia se não existir."""
    try:
        with open(_CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"especies": {}, "buscas": {}}


def _salvar_cache(cache: dict) -> None:
    """Persiste o cache no disco."""
    os.makedirs(os.path.dirname(_CACHE_PATH), exist_ok=True)
    with open(_CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Normalização e utilitários
# ---------------------------------------------------------------------------

def _frequencia_em_dias(watering: str) -> int:
    """Converte o campo textual de rega da API para um intervalo em dias."""
    if not watering:
        return 7
    return _MAPA_FREQUENCIA_REGA.get(watering.lower(), 7)


def _normalizar_especie(item: dict) -> dict:
    """Converte um item da resposta da API Perenual para o formato interno."""
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

    default_image = item.get("default_image") or {}
    imagem = default_image.get("medium_url") or default_image.get("thumbnail") or ""

    return {
        "id": str(item.get("id", "")),
        "nome_comum": item.get("common_name", nome_cientifico),
        "nome_cientifico": nome_cientifico,
        "frequencia_rega": _frequencia_em_dias(item.get("watering", "average")),
        "luz": luz,
        "temp_minima": temp_minima,
        "imagem": imagem,
    }


def _api_disponivel() -> bool:
    """Verifica se a chave de API está configurada."""
    return bool(_API_KEY)


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------

def buscar_especies(query: str) -> List[dict]:
    """Busca espécies de plantas pelo nome informado.

    Consulta o cache local antes de chamar a API. Salva os resultados obtidos
    da API no cache para evitar chamadas repetidas.

    Args:
        query: Termo de busca (nome comum ou científico da espécie).

    Returns:
        Lista de dicionários com os dados das espécies encontradas.
    """
    chave = query.lower().strip()

    cache = _carregar_cache()
    if chave in cache.get("buscas", {}):
        return cache["buscas"][chave]

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
        resultados = [_normalizar_especie(item) for item in dados.get("data", [])]

        if not resultados:
            return _buscar_fallback(query)

        cache.setdefault("buscas", {})[chave] = resultados
        for esp in resultados:
            cache.setdefault("especies", {})[esp["id"]] = esp
        _salvar_cache(cache)

        return resultados
    except requests.RequestException:
        return _buscar_fallback(query)


def obter_especie(id: str) -> Optional[dict]:
    """Retorna os detalhes completos de uma espécie pelo seu identificador.

    Consulta o cache local antes de chamar a API. Salva o resultado no cache.

    Args:
        id: Identificador da espécie (numérico da API ou ``local-N``).

    Returns:
        Dicionário com os dados da espécie, ou None se não encontrada.
    """
    if str(id).startswith("local-"):
        return _buscar_fallback_por_id(id)

    cache = _carregar_cache()
    if str(id) in cache.get("especies", {}):
        return cache["especies"][str(id)]

    if not _api_disponivel():
        return _buscar_fallback_por_id(id)

    try:
        resposta = requests.get(
            f"{_BASE_URL}/species/details/{id}",
            params={"key": _API_KEY},
            timeout=5,
        )
        resposta.raise_for_status()
        especie = _normalizar_especie(resposta.json())

        cache.setdefault("especies", {})[str(id)] = especie
        _salvar_cache(cache)

        return especie
    except requests.RequestException:
        return _buscar_fallback_por_id(id)


# ---------------------------------------------------------------------------
# Fallback local
# ---------------------------------------------------------------------------

def _normalizar_texto(texto: str) -> str:
    """Remove acentos e converte para minúsculas para comparação."""
    return unicodedata.normalize("NFD", texto).encode("ascii", "ignore").decode("ascii").lower()


def _buscar_fallback(query: str) -> List[dict]:
    """Filtra o catálogo local pelo termo de busca.

    Suporta busca parcial por palavras, sem distinção de maiúsculas/minúsculas
    e sem distinção de acentos. Cada palavra do termo deve aparecer em algum
    campo do nome da espécie.
    """
    palavras = _normalizar_texto(query).split()
    resultados = []
    for esp in _FALLBACK_ESPECIES:
        campo = _normalizar_texto(esp["nome_comum"]) + " " + _normalizar_texto(esp["nome_cientifico"])
        if all(p in campo for p in palavras):
            resultados.append(esp)
    return resultados


def _buscar_fallback_por_id(id: str) -> Optional[dict]:
    """Localiza uma espécie no catálogo local pelo identificador."""
    for esp in _FALLBACK_ESPECIES:
        if esp["id"] == str(id):
            return esp
    return None

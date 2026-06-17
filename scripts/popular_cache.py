"""Script para pré-popular o cache de espécies com plantas comuns no Brasil.

Execute uma vez para preencher data/especies_cache.json sem gastar chamadas
repetidas à API gratuita da Perenual:

    python scripts/popular_cache.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.especie_service import buscar_especies, _api_disponivel

PLANTAS_COMUNS_BRASIL = [
    "pothos",
    "monstera",
    "anthurium",
    "spathiphyllum",
    "sansevieria",
    "nephrolepis",
    "phalaenopsis",
    "cactus",
    "echeveria",
    "aloe vera",
    "kalanchoe",
    "ficus benjamina",
    "begonia",
    "saintpaulia",
    "dracaena marginata",
    "bromelia",
    "syngonium",
    "philodendron",
    "rhapis",
    "codiaeum",
]


def main():
    if not _api_disponivel():
        print("ERRO: Variável PERENUAL_API_KEY não configurada.")
        sys.exit(1)

    print(f"Iniciando pré-população do cache com {len(PLANTAS_COMUNS_BRASIL)} buscas...\n")

    total_especies = 0
    for planta in PLANTAS_COMUNS_BRASIL:
        print(f"  Buscando: {planta}...", end=" ")
        resultados = buscar_especies(planta)
        print(f"{len(resultados)} espécie(s) encontrada(s)")
        total_especies += len(resultados)

    print(f"\nCache populado com sucesso! Total acumulado: {total_especies} registro(s).")
    print("Arquivo: data/especies_cache.json")


if __name__ == "__main__":
    main()

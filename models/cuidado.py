"""Módulo de domínio para registros de cuidados de plantas."""

import uuid
from datetime import date


class Cuidado:
    """Classe base que representa um registro de cuidado realizado em uma planta.

    Attributes:
        id (str): Identificador único do registro.
        tipo (str): Tipo do cuidado (definido pelas subclasses).
        data (date): Data em que o cuidado foi realizado.
        observacao (str): Observação opcional sobre o cuidado.
    """

    tipo = "generico"

    def __init__(self, data: date, observacao: str = "", id: str = None):
        """Inicializa um Cuidado.

        Args:
            data: Data em que o cuidado foi realizado.
            observacao: Observação opcional sobre o cuidado.
            id: Identificador único; gerado automaticamente se não fornecido.
        """
        self.id = id or str(uuid.uuid4())
        self.data = data
        self.observacao = observacao

    def to_dict(self) -> dict:
        """Serializa o cuidado em dicionário para persistência JSON.

        Returns:
            Dicionário com todos os atributos do cuidado.
        """
        return {
            "id": self.id,
            "tipo": self.tipo,
            "data": self.data.isoformat(),
            "observacao": self.observacao,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Cuidado":
        """Instancia o tipo correto de Cuidado a partir de um dicionário JSON.

        Usa o campo ``tipo`` para determinar a subclasse adequada.

        Args:
            data: Dicionário com os atributos do cuidado.

        Returns:
            Instância da subclasse correspondente ao tipo registrado.
        """
        tipo = data.get("tipo", "generico")
        mapa = {
            Rega.tipo: Rega,
            Adubacao.tipo: Adubacao,
            Poda.tipo: Poda,
        }
        klass = mapa.get(tipo, Cuidado)
        return klass(
            id=data["id"],
            data=date.fromisoformat(data["data"]),
            observacao=data.get("observacao", ""),
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, data={self.data!r})"


class Rega(Cuidado):
    """Representa um registro de rega realizada na planta."""

    tipo = "rega"


class Adubacao(Cuidado):
    """Representa um registro de adubação realizada na planta."""

    tipo = "adubacao"


class Poda(Cuidado):
    """Representa um registro de poda realizada na planta."""

    tipo = "poda"

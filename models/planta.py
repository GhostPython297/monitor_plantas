"""Módulo de domínio para plantas monitoradas."""

import uuid
from datetime import date
from typing import List, Optional

from models.cuidado import Cuidado


class Planta:
    """Representa uma planta cadastrada e monitorada por um colaborador.

    Attributes:
        id (str): Identificador único da planta.
        nome (str): Nome dado pelo colaborador à planta.
        especie (dict): Dados da espécie vindos da API externa.
        frequencia_rega (int): Intervalo em dias entre regas recomendadas.
        colaborador_id (str): ID do colaborador responsável pela planta.
        historico_cuidados (list[Cuidado]): Lista de cuidados registrados.
        log_edicoes (list[dict]): Log de alterações realizadas na planta.
    """

    def __init__(
        self,
        nome: str,
        especie: dict,
        frequencia_rega: int,
        colaborador_id: str,
        historico_cuidados: List[Cuidado] = None,
        log_edicoes: List[dict] = None,
        id: str = None,
    ):
        """Inicializa uma Planta.

        Args:
            nome: Nome dado pelo colaborador à planta.
            especie: Dicionário com dados da espécie (nome_comum, nome_cientifico etc.).
            frequencia_rega: Intervalo em dias entre regas recomendadas.
            colaborador_id: ID do colaborador dono da planta.
            historico_cuidados: Lista de cuidados já registrados.
            log_edicoes: Lista de entradas de log de edições anteriores.
            id: Identificador único; gerado automaticamente se não fornecido.
        """
        self.id = id or str(uuid.uuid4())
        self.nome = nome
        self.especie = especie or {}
        self.frequencia_rega = int(frequencia_rega)
        self.colaborador_id = colaborador_id
        self.historico_cuidados: List[Cuidado] = historico_cuidados or []
        self.log_edicoes: List[dict] = log_edicoes or []

    def _data_ultimo_cuidado(self) -> Optional[date]:
        """Retorna a data do cuidado mais recente registrado.

        Returns:
            Data do último cuidado ou None se não houver nenhum.
        """
        if not self.historico_cuidados:
            return None
        return max(c.data for c in self.historico_cuidados)

    def dias_sem_cuidado(self) -> Optional[int]:
        """Calcula quantos dias se passaram desde o último cuidado registrado.

        Returns:
            Número de dias sem cuidado, ou None se não houver registros.
        """
        ultima = self._data_ultimo_cuidado()
        if ultima is None:
            return None
        return (date.today() - ultima).days

    def precisa_cuidado(self) -> bool:
        """Indica se a planta ultrapassou o intervalo de rega recomendado.

        Considera que uma planta sem nenhum registro também precisa de cuidado.

        Returns:
            True se o intervalo foi ultrapassado ou se não há registros.
        """
        dias = self.dias_sem_cuidado()
        if dias is None:
            return True
        return dias >= self.frequencia_rega

    def registrar_cuidado(self, cuidado: Cuidado) -> None:
        """Adiciona um cuidado ao histórico da planta.

        Args:
            cuidado: Instância de Cuidado (Rega, Adubacao ou Poda) a registrar.
        """
        self.historico_cuidados.append(cuidado)

    def to_dict(self) -> dict:
        """Serializa a planta em dicionário para persistência JSON.

        Returns:
            Dicionário com todos os atributos da planta.
        """
        return {
            "id": self.id,
            "nome": self.nome,
            "especie": self.especie,
            "frequencia_rega": self.frequencia_rega,
            "colaborador_id": self.colaborador_id,
            "historico_cuidados": [c.to_dict() for c in self.historico_cuidados],
            "log_edicoes": self.log_edicoes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Planta":
        """Instancia uma Planta a partir de um dicionário JSON.

        Args:
            data: Dicionário com os atributos da planta.

        Returns:
            Instância de Planta reconstruída com seu histórico de cuidados.
        """
        historico = [
            Cuidado.from_dict(c) for c in data.get("historico_cuidados", [])
        ]
        return cls(
            id=data["id"],
            nome=data["nome"],
            especie=data.get("especie", {}),
            frequencia_rega=data["frequencia_rega"],
            colaborador_id=data["colaborador_id"],
            historico_cuidados=historico,
            log_edicoes=data.get("log_edicoes", []),
        )

    def __repr__(self) -> str:
        return f"Planta(id={self.id!r}, nome={self.nome!r})"

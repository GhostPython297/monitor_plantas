"""Módulo de domínio para alertas de cuidado de plantas."""

from typing import Optional


class Alerta:
    """Representa um alerta gerado dinamicamente para uma planta que precisa de cuidado.

    Alertas não são persistidos; são derivados em tempo de execução a partir do
    estado atual das plantas pelo método ``precisa_cuidado()``.

    Attributes:
        planta_id (str): ID da planta que gerou o alerta.
        nome_planta (str): Nome da planta para exibição.
        dias_sem_cuidado (int | None): Dias desde o último cuidado registrado.
        frequencia_rega (int): Intervalo de rega configurado para a planta.
    """

    def __init__(
        self,
        planta_id: str,
        nome_planta: str,
        dias_sem_cuidado: Optional[int],
        frequencia_rega: int,
    ):
        """Inicializa um Alerta.

        Args:
            planta_id: ID da planta que gerou o alerta.
            nome_planta: Nome da planta para exibição na interface.
            dias_sem_cuidado: Dias desde o último cuidado; None se nunca cuidada.
            frequencia_rega: Intervalo em dias entre regas recomendadas.
        """
        self.planta_id = planta_id
        self.nome_planta = nome_planta
        self.dias_sem_cuidado = dias_sem_cuidado
        self.frequencia_rega = frequencia_rega

    @property
    def dias_atraso(self) -> Optional[int]:
        """Calcula quantos dias de atraso a planta acumula.

        Returns:
            Número de dias além do intervalo recomendado, ou None se sem registros.
        """
        if self.dias_sem_cuidado is None:
            return None
        atraso = self.dias_sem_cuidado - self.frequencia_rega
        return max(atraso, 0)

    @classmethod
    def from_planta(cls, planta) -> "Alerta":
        """Cria um Alerta a partir de uma instância de Planta.

        Args:
            planta: Instância de ``Planta`` que ultrapassou o intervalo de rega.

        Returns:
            Instância de Alerta correspondente à planta.
        """
        return cls(
            planta_id=planta.id,
            nome_planta=planta.nome,
            dias_sem_cuidado=planta.dias_sem_cuidado(),
            frequencia_rega=planta.frequencia_rega,
        )

    def __repr__(self) -> str:
        return (
            f"Alerta(planta_id={self.planta_id!r}, "
            f"nome_planta={self.nome_planta!r}, "
            f"dias_sem_cuidado={self.dias_sem_cuidado!r})"
        )

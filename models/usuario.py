"""Módulo de domínio para colaboradores do sistema."""

import hashlib
import uuid


class Colaborador:
    """Representa um colaborador cadastrado no sistema.

    Attributes:
        id (str): Identificador único do colaborador.
        nome (str): Nome completo do colaborador.
        email (str): Endereço de e-mail (usado como login).
        senha_hash (str): Hash SHA-256 da senha do colaborador.
    """

    def __init__(self, nome: str, email: str, senha_hash: str, id: str = None):
        """Inicializa um Colaborador.

        Args:
            nome: Nome completo do colaborador.
            email: Endereço de e-mail do colaborador.
            senha_hash: Hash SHA-256 da senha.
            id: Identificador único; gerado automaticamente se não fornecido.
        """
        self.id = id or str(uuid.uuid4())
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash

    @staticmethod
    def _hash_senha(senha: str) -> str:
        """Retorna o hash SHA-256 de uma senha em texto plano.

        Args:
            senha: Senha em texto plano.

        Returns:
            String hexadecimal com o hash SHA-256.
        """
        return hashlib.sha256(senha.encode("utf-8")).hexdigest()

    @classmethod
    def criar(cls, nome: str, email: str, senha: str) -> "Colaborador":
        """Cria um novo Colaborador aplicando hash na senha.

        Args:
            nome: Nome completo do colaborador.
            email: Endereço de e-mail do colaborador.
            senha: Senha em texto plano (será convertida para hash).

        Returns:
            Nova instância de Colaborador com senha hasheada.
        """
        return cls(nome=nome, email=email, senha_hash=cls._hash_senha(senha))

    def verificar_senha(self, senha: str) -> bool:
        """Verifica se a senha fornecida corresponde ao hash armazenado.

        Args:
            senha: Senha em texto plano a ser verificada.

        Returns:
            True se a senha estiver correta, False caso contrário.
        """
        return self.senha_hash == self._hash_senha(senha)

    def to_dict(self) -> dict:
        """Serializa o colaborador em dicionário para persistência JSON.

        Returns:
            Dicionário com todos os atributos do colaborador.
        """
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "senha_hash": self.senha_hash,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Colaborador":
        """Instancia um Colaborador a partir de um dicionário JSON.

        Args:
            data: Dicionário com os atributos do colaborador.

        Returns:
            Instância de Colaborador reconstruída.
        """
        return cls(
            id=data["id"],
            nome=data["nome"],
            email=data["email"],
            senha_hash=data["senha_hash"],
        )

    def __repr__(self) -> str:
        return f"Colaborador(id={self.id!r}, nome={self.nome!r}, email={self.email!r})"

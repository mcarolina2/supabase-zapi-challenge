"""Integração com o Supabase: leitura dos contatos cadastrados."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import List
from supabase import Client, create_client


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Contact:
    nome: str
    telefone: str


class SupabaseContactRepository:
    """Responsável por consultar contatos na tabela configurada do Supabase."""

    def __init__(self, url: str, key: str, table: str) -> None:
        self._client: Client = create_client(url, key)
        self._table = table

    def get_contacts(self, limit: int = 3) -> List[Contact]:
        """
        Retorna até `limit` contatos válidos (com nome e telefone preenchidos).

        Levanta a exceção original do client em caso de erro de conexão/consulta,
        para que o chamador decida como tratar (log + saída controlada).
        """
        logger.info("Buscando até %s contato(s) na tabela '%s'...", limit, self._table)

        response = (
            self._client.table(self._table)
            .select("nome, telefone")
            .limit(limit)
            .execute()
        )

        rows = response.data or []
        contacts = [
            Contact(nome=row["nome"], telefone=str(row["telefone"]))
            for row in rows
            if row.get("nome") and row.get("telefone")
        ]

        ignorados = len(rows) - len(contacts)
        if ignorados:
            logger.warning("%s registro(s) ignorado(s) por falta de nome/telefone.", ignorados)

        logger.info("%s contato(s) válido(s) encontrado(s).", len(contacts))
        return contacts

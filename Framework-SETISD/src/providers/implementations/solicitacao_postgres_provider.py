import os
from typing import List, Dict, Any
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ..interfaces.solicitacao_provider_interface import SolicitacaoProviderInterface
from .solicitacao_csv_provider import normalizar_item


def _ler_sql(nome: str) -> str:
    caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sql", nome)
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()


class SolicitacaoPostgresProvider(SolicitacaoProviderInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def listar_itens_solicitados(self) -> List[Dict[str, Any]]:
        resultado = await self.session.execute(text(_ler_sql("solicitacao/listar_itens_solicitados.sql")))
        return [normalizar_item(dict(linha)) for linha in resultado.mappings().all()]

    def descricao_fonte(self) -> str:
        return "AGHU (PostgreSQL, somente leitura)"

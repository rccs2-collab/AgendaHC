import csv
import os
from datetime import datetime
from typing import List, Dict, Any

from ..interfaces.solicitacao_provider_interface import SolicitacaoProviderInterface


def _parse_data(valor: str) -> str:
    for formato in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(valor.strip(), formato).isoformat()
        except ValueError:
            continue
    return valor.strip()


def normalizar_item(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "prontuario": str(row.get("prontuario") or "").strip(),
        "nome": str(row.get("nome") or "").strip(),
        "codigo_solicitacao": str(row.get("codigo_solicitacao") or "").strip(),
        "data_solicitacao": _parse_data(str(row.get("data_solicitao") or row.get("data_solicitacao") or "")),
        "unidade": str(row.get("unidade_solicitante") or "").strip(),
        "codigo_exame": str(row.get("codigo_exame") or "").strip(),
        "nome_exame": str(row.get("nome_exame") or "").strip(),
        "solicitante": str(row.get("nome_funcionario") or "").strip(),
    }


class SolicitacaoCsvProvider(SolicitacaoProviderInterface):
    def __init__(self, csv_path: str = "data/solicitacoes.csv"):
        self.csv_path = csv_path
        if not os.path.exists(csv_path):
            raise RuntimeError(f"Arquivo CSV de solicitações não encontrado em: {csv_path}")

    async def listar_itens_solicitados(self) -> List[Dict[str, Any]]:
        with open(self.csv_path, mode="r", encoding="utf-8") as f:
            return [normalizar_item(row) for row in csv.DictReader(f)]

    def descricao_fonte(self) -> str:
        atualizado = datetime.fromtimestamp(os.path.getmtime(self.csv_path))
        if "sintetic" in os.path.basename(self.csv_path):
            return f"Dados sintéticos no formato do extrato do AGHU (CSV) · arquivo de {atualizado:%d/%m/%Y}"
        return f"Extrato anonimizado do AGHU (CSV) · arquivo de {atualizado:%d/%m/%Y}"

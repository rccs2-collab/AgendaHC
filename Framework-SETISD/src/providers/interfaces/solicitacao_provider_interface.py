from abc import ABC, abstractmethod
from typing import List, Dict, Any


class SolicitacaoProviderInterface(ABC):

    @abstractmethod
    async def listar_itens_solicitados(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def descricao_fonte(self) -> str:
        pass

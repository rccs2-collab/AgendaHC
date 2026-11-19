import os
from datetime import date, datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.auth import auth_handler
from ..controllers import fila_controller as fila
from ..dependencies import get_solicitacao_provider
from ..helpers.audit_helper import registrar_auditoria
from ..models.agenda import TratamentoSolicitacao
from ..providers.interfaces.solicitacao_provider_interface import SolicitacaoProviderInterface
from ..resources.database import get_app_db_session

STRATEGY = os.getenv("SOLICITACAO_PROVIDER_TYPE", "csv")

router = APIRouter(
    prefix="/api/fila",
    tags=["Fila de marcação"],
    dependencies=[Depends(auth_handler.decode_token)],
)


class NovoTratamento(BaseModel):
    codigo_solicitacao: str
    codigo_exame: str
    status: str
    data_agendada: Optional[date] = None
    observacao: Optional[str] = None


def _contem(grupo, termo: str) -> bool:
    termo = termo.strip().lower()
    return termo in grupo["nome"].lower() or termo in grupo["prontuario"]


@router.get("")
async def obter_fila(
    unidade: Optional[str] = None,
    busca: Optional[str] = None,
    provider: SolicitacaoProviderInterface = Depends(get_solicitacao_provider(STRATEGY)),
    db: AsyncSession = Depends(get_app_db_session),
):
    hoje = date.today()
    itens = await provider.listar_itens_solicitados()
    ctx = await fila.carregar_contexto(db, hoje)
    resultado = fila.ranquear_fila(
        itens, ctx["status_atual"], ctx["prioritarios"], ctx["regras"], ctx["combinacoes"], hoje, unidade
    )
    grupos = resultado["grupos"]
    if busca:
        grupos = [g for g in grupos if _contem(g, busca)]
    return {
        "fonte": provider.descricao_fonte(),
        "gerado_em": datetime.now().isoformat(timespec="minutes"),
        "unidade": unidade,
        "regra": resultado["regra"],
        "resumo": resultado["resumo"],
        "unidades": fila.resumo_unidades(itens, ctx["status_atual"]),
        "total_exames": len(itens),
        "grupos": grupos,
    }


@router.get("/pacientes/{chave}")
async def obter_paciente(
    chave: str,
    provider: SolicitacaoProviderInterface = Depends(get_solicitacao_provider(STRATEGY)),
    db: AsyncSession = Depends(get_app_db_session),
):
    hoje = date.today()
    itens = [i for i in await provider.listar_itens_solicitados() if fila.chave_paciente(i) == chave]
    if not itens:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado na fila")
    ctx = await fila.carregar_contexto(db, hoje)
    todos = []
    for item in sorted(itens, key=lambda i: i["data_solicitacao"]):
        st = ctx["status_atual"].get(fila.chave_item(item))
        todos.append({
            **{k: v for k, v in item.items() if k not in ("prontuario", "nome")},
            "espera_dias": fila.dias_de_espera(item["data_solicitacao"], hoje),
            "status": st["status"] if st else "PENDENTE",
            "status_info": st,
        })
    prontuario = itens[0]["prontuario"]
    return {
        "chave": chave,
        "prontuario": prontuario,
        "nome": itens[0]["nome"],
        "itens": todos,
        "prioridades": [p for p in ctx["prioritarios"] if prontuario and p["prontuario"] == prontuario],
        "alertas": fila.detectar_combinacoes(
            (i["nome_exame"] for i in todos if i["status"] not in fila.STATUS_QUE_SAEM_DA_FILA), ctx["combinacoes"]
        ),
        "historico": await fila.historico_do_paciente(db, prontuario or chave),
        "dados_ausentes": ["data de retorno", "município", "telefone"],
    }


@router.post("/tratamentos", status_code=status.HTTP_201_CREATED)
async def registrar_tratamento(
    corpo: NovoTratamento,
    request: Request,
    usuario: dict = Depends(auth_handler.decode_token),
    provider: SolicitacaoProviderInterface = Depends(get_solicitacao_provider(STRATEGY)),
    db: AsyncSession = Depends(get_app_db_session),
):
    if corpo.status not in fila.STATUS_VALIDOS:
        raise HTTPException(status_code=400, detail=f"Status inválido: {corpo.status}")
    if corpo.status == "AGENDADO" and not corpo.data_agendada:
        raise HTTPException(status_code=400, detail="Informe a data agendada no AGHU.")
    item = next(
        (i for i in await provider.listar_itens_solicitados()
         if i["codigo_solicitacao"] == corpo.codigo_solicitacao and i["codigo_exame"] == corpo.codigo_exame),
        None,
    )
    if item is None:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada no AGHU")

    nome_usuario = usuario.get("sub") or usuario.get("username") or "desconhecido"
    anterior = (await fila.carregar_contexto(db, date.today()))["status_atual"].get(fila.chave_item(item))
    db.add(TratamentoSolicitacao(
        codigo_solicitacao=corpo.codigo_solicitacao,
        codigo_exame=corpo.codigo_exame,
        prontuario=item["prontuario"] or fila.chave_paciente(item),
        status=corpo.status,
        data_agendada=corpo.data_agendada,
        observacao=(corpo.observacao or "").strip() or None,
        usuario=nome_usuario,
    ))
    await db.commit()
    await registrar_auditoria(
        db=db,
        usuario=nome_usuario,
        categoria="NEGOCIO_CLINICO",
        acao="REGISTRAR_TRATAMENTO_SOLICITACAO",
        recurso=f"solicitacao:{corpo.codigo_solicitacao}:{corpo.codigo_exame}",
        dados_anteriores=anterior,
        dados_novos=corpo.model_dump(mode="json"),
        ip_origem=request.client.host if request.client else None,
    )
    return {"ok": True}

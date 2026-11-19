import os
from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.auth import auth_handler
from ..controllers import fila_controller as fila
from ..dependencies import get_solicitacao_provider
from ..helpers.audit_helper import registrar_auditoria
from ..models.agenda import PacientePrioritario, RegraPrioridade
from ..providers.interfaces.solicitacao_provider_interface import SolicitacaoProviderInterface
from ..resources.database import get_app_db_session

STRATEGY = os.getenv("SOLICITACAO_PROVIDER_TYPE", "csv")

router = APIRouter(
    prefix="/api",
    tags=["Regras e painel"],
    dependencies=[Depends(auth_handler.decode_token)],
)


class AtualizarRegra(BaseModel):
    unidade: str
    criterios: List[str]
    espera_limite_dias: int = Field(ge=1, le=365)


class NovoPrioritario(BaseModel):
    prontuario: str
    area: str
    motivo: str
    unidade: Optional[str] = None
    validade: Optional[date] = None


def _usuario(payload: dict) -> str:
    return payload.get("sub") or payload.get("username") or "desconhecido"


def _ip(request: Request) -> Optional[str]:
    return request.client.host if request.client else None


@router.get("/regras")
async def listar_regras(db: AsyncSession = Depends(get_app_db_session)):
    ctx = await fila.carregar_contexto(db, date.today())
    return {
        "criterios_disponiveis": list(fila.CRITERIOS_VALIDOS),
        "regras": sorted(ctx["regras"].values(), key=lambda r: (r["unidade"] != fila.REGRA_GERAL, r["unidade"])),
        "prioritarios": ctx["prioritarios"],
        "combinacoes": ctx["combinacoes"],
    }


@router.put("/regras")
async def atualizar_regra(
    corpo: AtualizarRegra,
    request: Request,
    usuario: dict = Depends(auth_handler.decode_token),
    db: AsyncSession = Depends(get_app_db_session),
):
    invalidos = [c for c in corpo.criterios if c not in fila.CRITERIOS_VALIDOS]
    if invalidos or len(set(corpo.criterios)) != len(corpo.criterios) or not corpo.criterios:
        raise HTTPException(status_code=400, detail="Critérios inválidos ou repetidos.")
    regra = (await db.execute(select(RegraPrioridade).where(RegraPrioridade.unidade == corpo.unidade))).scalar_one_or_none()
    if regra is None:
        raise HTTPException(status_code=404, detail="Regra não encontrada para a unidade")
    anterior = {"criterios": regra.criterios, "espera_limite_dias": regra.espera_limite_dias, "versao": regra.versao}
    regra.criterios = corpo.criterios
    regra.espera_limite_dias = corpo.espera_limite_dias
    regra.versao = regra.versao + 1
    regra.exemplo = False
    regra.atualizado_por = _usuario(usuario)
    await db.commit()
    await registrar_auditoria(
        db=db, usuario=_usuario(usuario), categoria="CONFIGURACAO", acao="ALTERAR_REGRA_PRIORIDADE",
        recurso=f"regra:{corpo.unidade}", dados_anteriores=anterior,
        dados_novos={"criterios": regra.criterios, "espera_limite_dias": regra.espera_limite_dias, "versao": regra.versao},
        ip_origem=_ip(request),
    )
    return {"ok": True, "versao": regra.versao}


@router.post("/regras/prioritarios", status_code=201)
async def incluir_prioritario(
    corpo: NovoPrioritario,
    request: Request,
    usuario: dict = Depends(auth_handler.decode_token),
    db: AsyncSession = Depends(get_app_db_session),
):
    if not corpo.prontuario.strip() or not corpo.area.strip() or not corpo.motivo.strip():
        raise HTTPException(status_code=400, detail="Prontuário, área e motivo são obrigatórios.")
    novo = PacientePrioritario(
        prontuario=corpo.prontuario.strip(), area=corpo.area.strip(), motivo=corpo.motivo.strip(),
        unidade=corpo.unidade, validade=corpo.validade, criado_por=_usuario(usuario),
    )
    db.add(novo)
    await db.commit()
    await registrar_auditoria(
        db=db, usuario=_usuario(usuario), categoria="NEGOCIO_CLINICO", acao="INCLUIR_PACIENTE_PRIORITARIO",
        recurso=f"prontuario:{novo.prontuario}", dados_novos=corpo.model_dump(mode="json"), ip_origem=_ip(request),
    )
    return {"ok": True, "id": novo.id}


@router.delete("/regras/prioritarios/{prioritario_id}")
async def remover_prioritario(
    prioritario_id: int,
    request: Request,
    usuario: dict = Depends(auth_handler.decode_token),
    db: AsyncSession = Depends(get_app_db_session),
):
    registro = await db.get(PacientePrioritario, prioritario_id)
    if registro is None or not registro.ativo:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    registro.ativo = False
    await db.commit()
    await registrar_auditoria(
        db=db, usuario=_usuario(usuario), categoria="NEGOCIO_CLINICO", acao="REMOVER_PACIENTE_PRIORITARIO",
        recurso=f"prontuario:{registro.prontuario}", dados_anteriores={"area": registro.area, "ativo": True},
        dados_novos={"ativo": False}, ip_origem=_ip(request),
    )
    return {"ok": True}


@router.get("/painel")
async def obter_painel(
    provider: SolicitacaoProviderInterface = Depends(get_solicitacao_provider(STRATEGY)),
    db: AsyncSession = Depends(get_app_db_session),
):
    hoje = date.today()
    itens = await provider.listar_itens_solicitados()
    ctx = await fila.carregar_contexto(db, hoje)
    painel = fila.montar_painel(itens, ctx["status_atual"], await fila.contagem_status(db), hoje)
    painel["fonte"] = provider.descricao_fonte()
    return painel

from collections import defaultdict
from datetime import date, datetime
from statistics import median
from typing import Any, Dict, Iterable, List, Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.agenda import (
    CombinacaoExames,
    PacientePrioritario,
    RegraPrioridade,
    TratamentoSolicitacao,
)

CRITERIOS_VALIDOS = ("LISTA_PRIORIDADE", "ESPERA_LIMITE", "ORDEM_CHEGADA")
CRITERIOS_PADRAO = ["LISTA_PRIORIDADE", "ESPERA_LIMITE", "ORDEM_CHEGADA"]
STATUS_VALIDOS = ("EM_CONTATO", "SEM_CONTATO", "AGENDADO", "CANCELADO", "PENDENTE")
STATUS_QUE_SAEM_DA_FILA = ("AGENDADO", "CANCELADO")
REGRA_GERAL = "*"

Chave = Tuple[str, str]


def chave_item(item: Dict[str, Any]) -> Chave:
    return (item["codigo_solicitacao"], item["codigo_exame"])


def chave_paciente(item: Dict[str, Any]) -> str:
    return item["prontuario"] or f"sem-prontuario:{item['codigo_solicitacao']}"


def dias_de_espera(data_iso: str, hoje: date) -> int:
    try:
        return max((hoje - datetime.fromisoformat(data_iso).date()).days, 0)
    except ValueError:
        return 0


def regra_da_unidade(regras: Dict[str, Dict[str, Any]], unidade: Optional[str]) -> Dict[str, Any]:
    regra = regras.get(unidade or REGRA_GERAL) or regras.get(REGRA_GERAL)
    return regra or {"unidade": REGRA_GERAL, "criterios": CRITERIOS_PADRAO, "espera_limite_dias": 60, "versao": 0}


def prioridade_do_paciente(
    prontuario: str, unidade: Optional[str], prioritarios: Iterable[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    for p in prioritarios:
        if p["prontuario"] == prontuario and (not p.get("unidade") or not unidade or p["unidade"] == unidade):
            return p
    return None


def _chave_ordenacao(item, regra, prioritario) -> Tuple[tuple, Dict[str, Any]]:
    valores = []
    motivo = None
    for criterio in list(regra["criterios"]) + ["ORDEM_CHEGADA"]:
        if criterio == "LISTA_PRIORIDADE":
            atende = prioritario is not None
            valores.append(0 if atende else 1)
            if atende and motivo is None:
                motivo = {
                    "tipo": "LISTA",
                    "rotulo": f"Lista · {prioritario['area']}",
                    "detalhe": prioritario["motivo"],
                }
        elif criterio == "ESPERA_LIMITE":
            atende = item["espera_dias"] >= regra["espera_limite_dias"]
            valores.append(0 if atende else 1)
            if atende and motivo is None:
                motivo = {
                    "tipo": "ESPERA",
                    "rotulo": f"Espera > {regra['espera_limite_dias']} dias",
                    "detalhe": f"Aguarda há {item['espera_dias']} dias",
                }
        elif criterio == "ORDEM_CHEGADA":
            valores.append(item["data_solicitacao"])
    valores.append(item["codigo_solicitacao"])
    if motivo is None:
        motivo = {
            "tipo": "CHEGADA",
            "rotulo": "Ordem de chegada",
            "detalhe": f"Solicitado há {item['espera_dias']} dias",
        }
    return tuple(valores), motivo


def detectar_combinacoes(nomes_exames: Iterable[str], combinacoes: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    presentes = set(nomes_exames)
    alertas = []
    for c in combinacoes:
        if c["exame_a"] in presentes and c["exame_b"] in presentes:
            alertas.append({
                "tipo": c["tipo"],
                "orientacao": c["orientacao"],
                "exames": [c["exame_a"], c["exame_b"]],
                "exemplo": c.get("exemplo", False),
            })
    return alertas


def ranquear_fila(
    itens: List[Dict[str, Any]],
    status_atual: Dict[Chave, Dict[str, Any]],
    prioritarios: List[Dict[str, Any]],
    regras: Dict[str, Dict[str, Any]],
    combinacoes: List[Dict[str, Any]],
    hoje: date,
    unidade: Optional[str] = None,
) -> Dict[str, Any]:
    regra = regra_da_unidade(regras, unidade)
    pendentes_por_paciente: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for bruto in itens:
        st = status_atual.get(chave_item(bruto))
        if st and st["status"] in STATUS_QUE_SAEM_DA_FILA:
            continue
        item = dict(bruto)
        item["espera_dias"] = dias_de_espera(item["data_solicitacao"], hoje)
        item["status"] = st["status"] if st else "PENDENTE"
        item["status_info"] = st
        item["na_unidade"] = unidade is None or item["unidade"] == unidade
        pendentes_por_paciente[chave_paciente(item)].append(item)

    grupos = []
    for chave, lista in pendentes_por_paciente.items():
        no_escopo = [i for i in lista if i["na_unidade"]]
        if not no_escopo:
            continue
        prontuario = lista[0]["prontuario"]
        prioritario = prioridade_do_paciente(prontuario, unidade, prioritarios) if prontuario else None
        avaliados = [(*_chave_ordenacao(i, regra, prioritario), i) for i in no_escopo]
        avaliados.sort(key=lambda t: t[0])
        melhor_chave, motivo, _ = avaliados[0]
        ordenados = [t[2] for t in avaliados] + sorted(
            (i for i in lista if not i["na_unidade"]), key=lambda i: i["data_solicitacao"]
        )
        grupos.append({
            "chave": chave,
            "prontuario": prontuario,
            "nome": lista[0]["nome"],
            "sem_prontuario": not prontuario,
            "motivo": motivo,
            "prioridade": prioritario,
            "espera_dias": max(i["espera_dias"] for i in no_escopo),
            "itens": [
                {k: v for k, v in i.items() if k not in ("prontuario", "nome")} for i in ordenados
            ],
            "alertas": detectar_combinacoes((i["nome_exame"] for i in lista), combinacoes),
            "_ordem": melhor_chave,
        })

    grupos.sort(key=lambda g: g["_ordem"])
    for posicao, g in enumerate(grupos, start=1):
        g["posicao"] = posicao
        del g["_ordem"]

    esperas = [i["espera_dias"] for g in grupos for i in g["itens"] if i["na_unidade"]]
    return {
        "regra": regra,
        "grupos": grupos,
        "resumo": {
            "pacientes": len(grupos),
            "exames": len(esperas),
            "prioritarios": sum(1 for g in grupos if g["motivo"]["tipo"] == "LISTA"),
            "com_alerta": sum(1 for g in grupos if any(a["tipo"] != "AGRUPAR" for a in g["alertas"])),
            "espera_mediana": int(median(esperas)) if esperas else 0,
            "espera_maxima": max(esperas) if esperas else 0,
        },
    }


def resumo_unidades(itens, status_atual) -> List[Dict[str, Any]]:
    contagem: Dict[str, Dict[str, Any]] = {}
    for item in itens:
        st = status_atual.get(chave_item(item))
        if st and st["status"] in STATUS_QUE_SAEM_DA_FILA:
            continue
        u = contagem.setdefault(item["unidade"], {"unidade": item["unidade"], "exames": 0, "pacientes": set()})
        u["exames"] += 1
        u["pacientes"].add(chave_paciente(item))
    return sorted(
        ({"unidade": u["unidade"], "exames": u["exames"], "pacientes": len(u["pacientes"])} for u in contagem.values()),
        key=lambda u: -u["exames"],
    )


def montar_painel(itens, status_atual, historico_status, hoje: date) -> Dict[str, Any]:
    por_unidade: Dict[str, Dict[str, Any]] = {}
    for item in itens:
        u = por_unidade.setdefault(item["unidade"], {
            "unidade": item["unidade"], "pendentes": 0, "esperas": [], "faixas": [0, 0, 0, 0], "tratados": 0,
            "exames": defaultdict(int),
        })
        st = status_atual.get(chave_item(item))
        if st and st["status"] in STATUS_QUE_SAEM_DA_FILA:
            u["tratados"] += 1
            continue
        espera = dias_de_espera(item["data_solicitacao"], hoje)
        u["pendentes"] += 1
        u["esperas"].append(espera)
        u["faixas"][0 if espera <= 30 else 1 if espera <= 60 else 2 if espera <= 90 else 3] += 1
        u["exames"][item["nome_exame"]] += 1

    unidades = []
    for u in sorted(por_unidade.values(), key=lambda u: -u["pendentes"]):
        esperas = u.pop("esperas")
        exames = u.pop("exames")
        u["espera_mediana"] = int(median(esperas)) if esperas else 0
        u["espera_maxima"] = max(esperas) if esperas else 0
        u["acima_60"] = sum(1 for e in esperas if e > 60)
        u["principais_exames"] = sorted(
            ({"exame": k, "pendentes": v} for k, v in exames.items()), key=lambda e: -e["pendentes"]
        )[:3]
        unidades.append(u)

    return {
        "unidades": unidades,
        "totais": {
            "pendentes": sum(u["pendentes"] for u in unidades),
            "tratados": sum(u["tratados"] for u in unidades),
            "acima_60": sum(u["acima_60"] for u in unidades),
            "faixas": [sum(u["faixas"][i] for u in unidades) for i in range(4)],
        },
        "status": historico_status,
    }


async def carregar_contexto(session: AsyncSession, hoje: date) -> Dict[str, Any]:
    tratamentos = (await session.execute(
        select(TratamentoSolicitacao).order_by(TratamentoSolicitacao.criado_em, TratamentoSolicitacao.id)
    )).scalars().all()
    status_atual: Dict[Chave, Dict[str, Any]] = {}
    for t in tratamentos:
        status_atual[(t.codigo_solicitacao, t.codigo_exame)] = {
            "status": t.status,
            "data_agendada": t.data_agendada.isoformat() if t.data_agendada else None,
            "observacao": t.observacao,
            "usuario": t.usuario,
            "criado_em": t.criado_em.isoformat(),
        }

    prioritarios = [
        {
            "id": p.id, "prontuario": p.prontuario, "area": p.area, "motivo": p.motivo, "unidade": p.unidade,
            "validade": p.validade.isoformat() if p.validade else None, "exemplo": p.exemplo,
        }
        for p in (await session.execute(
            select(PacientePrioritario).where(PacientePrioritario.ativo.is_(True)).order_by(PacientePrioritario.id)
        )).scalars().all()
        if p.validade is None or p.validade >= hoje
    ]

    regras = {
        r.unidade: {
            "unidade": r.unidade, "criterios": r.criterios, "espera_limite_dias": r.espera_limite_dias,
            "versao": r.versao, "exemplo": r.exemplo, "atualizado_por": r.atualizado_por,
            "atualizado_em": r.atualizado_em.isoformat() if r.atualizado_em else None,
        }
        for r in (await session.execute(select(RegraPrioridade))).scalars().all()
    }

    combinacoes = [
        {"id": c.id, "exame_a": c.exame_a, "exame_b": c.exame_b, "tipo": c.tipo, "orientacao": c.orientacao,
         "exemplo": c.exemplo}
        for c in (await session.execute(
            select(CombinacaoExames).where(CombinacaoExames.ativo.is_(True)).order_by(CombinacaoExames.id)
        )).scalars().all()
    ]

    return {"status_atual": status_atual, "prioritarios": prioritarios, "regras": regras, "combinacoes": combinacoes}


async def historico_do_paciente(session: AsyncSession, prontuario: str) -> List[Dict[str, Any]]:
    linhas = (await session.execute(
        select(TratamentoSolicitacao)
        .where(TratamentoSolicitacao.prontuario == prontuario)
        .order_by(TratamentoSolicitacao.criado_em.desc(), TratamentoSolicitacao.id.desc())
    )).scalars().all()
    return [
        {
            "codigo_solicitacao": t.codigo_solicitacao, "codigo_exame": t.codigo_exame, "status": t.status,
            "data_agendada": t.data_agendada.isoformat() if t.data_agendada else None,
            "observacao": t.observacao, "usuario": t.usuario, "criado_em": t.criado_em.isoformat(),
        }
        for t in linhas
    ]


async def contagem_status(session: AsyncSession) -> Dict[str, int]:
    rows = (await session.execute(
        select(TratamentoSolicitacao.status, func.count()).group_by(TratamentoSolicitacao.status)
    )).all()
    return {status: total for status, total in rows}


COMBINACOES_EXEMPLO = [
    ("CINTILOGRAFIA DO MIOCARDIO EM REPOUSO", "CINTILOGRAFIA DO MIOCARDIO COM DIPIRIDAMOL", "AGRUPAR",
     "Repouso e estresse fazem parte do mesmo protocolo: agendar em sequência."),
    ("CINTILOGRAFIA RENAL COM DMSA", "CINTILOGRAFIA RENALCOM DTPA", "SEPARAR",
     "Radiofármacos diferentes: não agendar no mesmo dia."),
    ("BIÓPSIA ORIENTADA POR ECOGRAFIA - MAMA", "ANATOMOPATOLÓGICO - MAMA", "ORDEM",
     "O anatomopatológico depende do material da biópsia: biópsia primeiro."),
    ("DENSITOMETRIA ÓSSEA", "CINTILOGRAFIA DO ESQUELETO", "SEPARAR",
     "Radiofármaco interfere na densitometria: densitometria antes ou com intervalo."),
    ("AUDIOMETRIA TONAL LIMIAR (VIA AÉREA/VIA ÓSSEA)", "IMITANCIOMETRIA", "AGRUPAR",
     "Bateria audiológica: agendar no mesmo atendimento."),
    ("AUDIOMETRIA TONAL LIMIAR (VIA AÉREA/VIA ÓSSEA)", "LOGOAUDIOMETRIA", "AGRUPAR",
     "Bateria audiológica: agendar no mesmo atendimento."),
]


async def semear_dados_exemplo(session: AsyncSession, itens: List[Dict[str, Any]]) -> None:
    if (await session.execute(select(func.count()).select_from(RegraPrioridade))).scalar_one() == 0:
        session.add(RegraPrioridade(
            unidade=REGRA_GERAL, criterios=CRITERIOS_PADRAO, espera_limite_dias=60, versao=1, exemplo=True,
            atualizado_por="sistema",
        ))
        for unidade in sorted({i["unidade"] for i in itens}):
            session.add(RegraPrioridade(
                unidade=unidade, criterios=CRITERIOS_PADRAO, espera_limite_dias=60, versao=1, exemplo=True,
                atualizado_por="sistema",
            ))

    if (await session.execute(select(func.count()).select_from(CombinacaoExames))).scalar_one() == 0:
        for a, b, tipo, orientacao in COMBINACOES_EXEMPLO:
            session.add(CombinacaoExames(exame_a=a, exame_b=b, tipo=tipo, orientacao=orientacao, exemplo=True))

    if (await session.execute(select(func.count()).select_from(PacientePrioritario))).scalar_one() == 0:
        def escolher(codigos: Tuple[str, ...], quantidade: int) -> List[Dict[str, Any]]:
            vistos, escolhidos = set(), []
            for item in sorted(itens, key=lambda i: (i["data_solicitacao"], i["codigo_solicitacao"]), reverse=True):
                if item["codigo_exame"] in codigos and item["prontuario"] and item["prontuario"] not in vistos:
                    vistos.add(item["prontuario"])
                    escolhidos.append(item)
                if len(escolhidos) == quantidade:
                    break
            return escolhidos

        for item in escolher(("CRDMS", "CRDTP"), 3):
            session.add(PacientePrioritario(
                prontuario=item["prontuario"], area="Nefrologia", motivo="Paciente em hemodiálise",
                unidade=item["unidade"], exemplo=True, criado_por="sistema",
            ))
        for item in escolher(("USBI4", "MBIOP"), 3):
            session.add(PacientePrioritario(
                prontuario=item["prontuario"], area="Oncologia", motivo="Suspeita oncológica",
                unidade=item["unidade"], exemplo=True, criado_por="sistema",
            ))

    await session.commit()

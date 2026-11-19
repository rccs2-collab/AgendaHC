from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, JSON

from ..resources.database import Base


def _agora():
    return datetime.now(timezone.utc)


class TratamentoSolicitacao(Base):
    __tablename__ = "tratamentos_solicitacao"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_solicitacao = Column(String, nullable=False, index=True)
    codigo_exame = Column(String, nullable=False, index=True)
    prontuario = Column(String, nullable=False, index=True)
    status = Column(String, nullable=False)
    data_agendada = Column(Date, nullable=True)
    observacao = Column(Text, nullable=True)
    usuario = Column(String, nullable=False)
    criado_em = Column(DateTime, default=_agora, nullable=False)


class PacientePrioritario(Base):
    __tablename__ = "pacientes_prioritarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    prontuario = Column(String, nullable=False, index=True)
    area = Column(String, nullable=False)
    motivo = Column(String, nullable=False)
    unidade = Column(String, nullable=True)
    validade = Column(Date, nullable=True)
    ativo = Column(Boolean, default=True, nullable=False)
    exemplo = Column(Boolean, default=False, nullable=False)
    criado_por = Column(String, nullable=False)
    criado_em = Column(DateTime, default=_agora, nullable=False)


class RegraPrioridade(Base):
    __tablename__ = "regras_prioridade"

    id = Column(Integer, primary_key=True, autoincrement=True)
    unidade = Column(String, nullable=False, unique=True, index=True)
    criterios = Column(JSON, nullable=False)
    espera_limite_dias = Column(Integer, nullable=False, default=60)
    versao = Column(Integer, nullable=False, default=1)
    exemplo = Column(Boolean, default=False, nullable=False)
    atualizado_por = Column(String, nullable=False)
    atualizado_em = Column(DateTime, default=_agora, onupdate=_agora, nullable=False)


class CombinacaoExames(Base):
    __tablename__ = "combinacoes_exames"

    id = Column(Integer, primary_key=True, autoincrement=True)
    exame_a = Column(String, nullable=False)
    exame_b = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    orientacao = Column(String, nullable=False)
    exemplo = Column(Boolean, default=False, nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)

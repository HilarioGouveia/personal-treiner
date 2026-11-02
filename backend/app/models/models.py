from datetime import date, datetime
import enum
from typing import Optional
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    Date,
    DateTime,
    Enum as SQLEnum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class PerfilUsuario(str, enum.Enum):
  PERSONAL = "PERSONAL"
  ALUNO = "ALUNO"


class StatusMensalidade(str, enum.Enum):
  PAGO = "PAGO"
  PENDENTE = "PENDENTE"
  ATRASADO = "ATRASADO"


class Usuario(Base):
  __tablename__ = "usuarios"

  id = Column(Integer, primary_key=True, index=True)
  email = Column(String(255), unique=True, nullable=False, index=True)
  senha_hash = Column(String(255), nullable=False)
  perfil = Column(
      SQLEnum(PerfilUsuario), nullable=False, default=PerfilUsuario.ALUNO
  )
  ativo = Column(Boolean, default=True, nullable=False)
  criado_em = Column(DateTime, default=datetime.utcnow)

  aluno = relationship("Aluno", back_populates="usuario", uselist=False)


class Aluno(Base):
  __tablename__ = "alunos"

  id = Column(Integer, primary_key=True, index=True)
  usuario_id = Column(
      Integer, ForeignKey("usuarios.id"), unique=True, nullable=False
  )
  nome = Column(String(150), nullable=False)
  data_nascimento = Column(Date, nullable=True)
  telefone = Column(String(20), nullable=True)
  objetivo = Column(String(255), nullable=True)
  observacoes_medicas = Column(Text, nullable=True)
  criado_em = Column(DateTime, default=datetime.utcnow)

  usuario = relationship("Usuario", back_populates="aluno")
  fichas_treino = relationship(
      "FichaTreino", back_populates="aluno", cascade="all, delete-orphan"
  )
  avaliacoes = relationship(
      "AvaliacaoFisica", back_populates="aluno", cascade="all, delete-orphan"
  )
  mensalidades = relationship(
      "Mensalidade", back_populates="aluno", cascade="all, delete-orphan"
  )


class Exercicio(Base):
  __tablename__ = "exercicios"

  id = Column(Integer, primary_key=True, index=True)
  nome = Column(String(150), nullable=False, index=True)
  grupo_muscular = Column(String(100), nullable=False)
  url_video = Column(String(255), nullable=True)

  itens_treino = relationship("ItemTreino", back_populates="exercicio")


class FichaTreino(Base):
  __tablename__ = "fichas_treino"

  id = Column(Integer, primary_key=True, index=True)
  aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
  titulo = Column(String(150), nullable=False)
  descricao = Column(Text, nullable=True)
  ativa = Column(Boolean, default=True, nullable=False)
  criada_em = Column(DateTime, default=datetime.utcnow)

  aluno = relationship("Aluno", back_populates="fichas_treino")
  itens = relationship(
      "ItemTreino", back_populates="ficha", cascade="all, delete-orphan"
  )


class ItemTreino(Base):
  __tablename__ = "itens_treino"

  id = Column(Integer, primary_key=True, index=True)
  ficha_id = Column(Integer, ForeignKey("fichas_treino.id"), nullable=False)
  exercicio_id = Column(Integer, ForeignKey("exercicios.id"), nullable=False)
  divisao = Column(String(5), nullable=False)  # Ex: "A", "B", "C"
  series = Column(Integer, nullable=False, default=3)
  repeticoes = Column(String(50), nullable=False)
  carga_kg = Column(Float, nullable=True)
  descanso_segundos = Column(Integer, default=60)
  ordem = Column(Integer, default=1)
  observacoes = Column(String(255), nullable=True)

  ficha = relationship("FichaTreino", back_populates="itens")
  exercicio = relationship("Exercicio", back_populates="itens_treino")


class AvaliacaoFisica(Base):
  __tablename__ = "avaliacoes_fisicas"

  id = Column(Integer, primary_key=True, index=True)
  aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
  data_avaliacao = Column(Date, default=date.today, nullable=False)
  peso_kg = Column(Float, nullable=False)
  altura_cm = Column(Float, nullable=True)
  percentual_gordura = Column(Float, nullable=True)
  medidas_json = Column(JSON, nullable=True)
  observacoes = Column(Text, nullable=True)

  aluno = relationship("Aluno", back_populates="avaliacoes")


class Mensalidade(Base):
  __tablename__ = "mensalidades"

  id = Column(Integer, primary_key=True, index=True)
  aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
  data_vencimento = Column(Date, nullable=False)
  valor = Column(Float, nullable=False)
  status = Column(
      SQLEnum(StatusMensalidade),
      default=StatusMensalidade.PENDENTE,
      nullable=False,
  )
  data_pagamento = Column(Date, nullable=True)

  aluno = relationship("Aluno", back_populates="mensalidades")

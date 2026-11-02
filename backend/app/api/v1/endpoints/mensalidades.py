from datetime import date
from typing import List
from app.core.database import get_db
from app.models.models import Aluno, Mensalidade, StatusMensalidade
from app.schemas.schemas import (
    MensalidadeCreate,
    MensalidadeResponse,
    MensalidadeUpdate,
)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/",
    response_model=MensalidadeResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_mensalidade(
    mensalidade_in: MensalidadeCreate, db: Session = Depends(get_db)
):
  aluno = db.query(Aluno).filter(Aluno.id == mensalidade_in.aluno_id).first()
  if not aluno:
    raise HTTPException(status_code=404, detail="Aluno não encontrado.")

  nova_mensalidade = Mensalidade(
      aluno_id=mensalidade_in.aluno_id,
      data_vencimento=mensalidade_in.data_vencimento,
      valor=mensalidade_in.valor,
      status=mensalidade_in.status,
      data_pagamento=mensalidade_in.data_pagamento,
  )

  db.add(nova_mensalidade)
  db.commit()
  db.refresh(nova_mensalidade)
  return nova_mensalidade


@router.get("/aluno/{aluno_id}", response_model=List[MensalidadeResponse])
def listar_mensalidades_aluno(aluno_id: int, db: Session = Depends(get_db)):
  return (
      db.query(Mensalidade)
      .filter(Mensalidade.aluno_id == aluno_id)
      .order_by(Mensalidade.data_vencimento.desc())
      .all()
  )


@router.patch("/{mensalidade_id}", response_model=MensalidadeResponse)
def atualizar_status_mensalidade(
    mensalidade_id: int,
    dados_atualizacao: MensalidadeUpdate,
    db: Session = Depends(get_db),
):
  mensalidade = (
      db.query(Mensalidade).filter(Mensalidade.id == mensalidade_id).first()
  )
  if not mensalidade:
    raise HTTPException(status_code=404, detail="Mensalidade não encontrada.")

  if dados_atualizacao.status:
    mensalidade.status = dados_atualizacao.status
    if dados_atualizacao.status == StatusMensalidade.PAGO:
      mensalidade.data_pagamento = dados_atualizacao.data_pagamento or date.today()

  db.commit()
  db.refresh(mensalidade)
  return mensalidade
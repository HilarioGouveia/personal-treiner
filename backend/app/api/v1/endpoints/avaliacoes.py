from typing import List
from app.core.database import get_db
from app.models.models import Aluno, AvaliacaoFisica
from app.schemas.schemas import AvaliacaoFisicaCreate, AvaliacaoFisicaResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/",
    response_model=AvaliacaoFisicaResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_avaliacao(
    avaliacao_in: AvaliacaoFisicaCreate, db: Session = Depends(get_db)
):
  # 1. Valida se o aluno existe
  aluno = db.query(Aluno).filter(Aluno.id == avaliacao_in.aluno_id).first()
  if not aluno:
    raise HTTPException(status_code=404, detail="Aluno não encontrado.")

  # 2. Cria o registro de avaliação física
  nova_avaliacao = AvaliacaoFisica(
      aluno_id=avaliacao_in.aluno_id,
      data_avaliacao=avaliacao_in.data_avaliacao or date.today(),
      peso_kg=avaliacao_in.peso_kg,
      altura_cm=avaliacao_in.altura_cm,
      percentual_gordura=avaliacao_in.percentual_gordura,
      medidas_json=avaliacao_in.medidas_json,
      observacoes=avaliacao_in.observacoes,
  )

  db.add(nova_avaliacao)
  db.commit()
  db.refresh(nova_avaliacao)
  return nova_avaliacao


@router.get("/aluno/{aluno_id}", response_model=List[AvaliacaoFisicaResponse])
def listar_avaliacoes_por_aluno(aluno_id: int, db: Session = Depends(get_db)):
  avaliacoes = (
      db.query(AvaliacaoFisica)
      .filter(AvaliacaoFisica.aluno_id == aluno_id)
      .order_by(AvaliacaoFisica.data_avaliacao.asc())
      .all()
  )
  return avaliacoes
from typing import List
from app.core.database import get_db
from app.models.models import Aluno, Exercicio, FichaTreino, ItemTreino
from app.schemas.schemas import (
    ExercicioCreate,
    ExercicioResponse,
    FichaTreinoCreate,
    FichaTreinoResponse,
)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


# ==========================================
# CATÁLOGO DE EXERCÍCIOS
# ==========================================
@router.post(
    "/exercicios/",
    response_model=ExercicioResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_exercicio(
    exercicio_in: ExercicioCreate, db: Session = Depends(get_db)
):
  novo_exercicio = Exercicio(
      nome=exercicio_in.nome,
      grupo_muscular=exercicio_in.grupo_muscular,
      url_video=exercicio_in.url_video,
  )
  db.add(novo_exercicio)
  db.commit()
  db.refresh(novo_exercicio)
  return novo_exercicio


@router.get("/exercicios/", response_model=List[ExercicioResponse])
def listar_exercicios(db: Session = Depends(get_db)):
  return db.query(Exercicio).all()


# ==========================================
# FICHAS DE TREINO
# ==========================================
@router.post(
    "/fichas/",
    response_model=FichaTreinoResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_ficha_treino(
    ficha_in: FichaTreinoCreate, db: Session = Depends(get_db)
):
  # 1. Valida se o aluno existe
  aluno = db.query(Aluno).filter(Aluno.id == ficha_in.aluno_id).first()
  if not aluno:
    raise HTTPException(status_code=404, detail="Aluno não encontrado.")

  # 2. Cria o cabeçalho da Ficha de Treino
  nova_ficha = FichaTreino(
      aluno_id=ficha_in.aluno_id,
      titulo=ficha_in.titulo,
      descricao=ficha_in.descricao,
      ativa=True,
  )
  db.add(nova_ficha)
  db.commit()
  db.refresh(nova_ficha)

  # 3. Adiciona os itens (exercícios prescritos) à ficha
  for item in ficha_in.itens:
    novo_item = ItemTreino(
        ficha_id=nova_ficha.id,
        exercicio_id=item.exercicio_id,
        divisao=item.divisao,
        series=item.series,
        repeticoes=item.repeticoes,
        carga_kg=item.carga_kg,
        descanso_segundos=item.descanso_segundos,
        ordem=item.ordem,
        observacoes=item.observacoes,
    )
    db.add(novo_item)

  db.commit()
  db.refresh(nova_ficha)
  return nova_ficha


@router.get(
    "/fichas/aluno/{aluno_id}", response_model=List[FichaTreinoResponse]
)
def listar_fichas_por_aluno(aluno_id: int, db: Session = Depends(get_db)):
  fichas = db.query(FichaTreino).filter(FichaTreino.aluno_id == aluno_id).all()
  return fichas
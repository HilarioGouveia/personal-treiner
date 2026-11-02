from typing import List
from app.core.database import get_db
from app.models.models import Aluno, PerfilUsuario, Usuario
from app.schemas.schemas import AlunoCreate, AlunoResponse
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/", response_model=AlunoResponse, status_code=status.HTTP_201_CREATED)
def criar_aluno(aluno_in: AlunoCreate, db: Session = Depends(get_db)):
  # Verifica se o email já existe
  usuario_existente = (
      db.query(Usuario).filter(Usuario.email == aluno_in.email).first()
  )
  if usuario_existente:
    raise HTTPException(status_code=400, detail="E-mail já cadastrado no sistema.")

  # Cria o registro de usuário
  hashed_password = pwd_context.hash(aluno_in.senha)
  novo_usuario = Usuario(
      email=aluno_in.email,
      senha_hash=hashed_password,
      perfil=PerfilUsuario.ALUNO,
  )
  db.add(novo_usuario)
  db.commit()
  db.refresh(novo_usuario)

  # Cria o perfil de aluno vinculado ao usuário
  novo_aluno = Aluno(
      usuario_id=novo_usuario.id,
      nome=aluno_in.nome,
      data_nascimento=aluno_in.data_nascimento,
      telefone=aluno_in.telefone,
      objetivo=aluno_in.objetivo,
      observacoes_medicas=aluno_in.observacoes_medicas,
  )
  db.add(novo_aluno)
  db.commit()
  db.refresh(novo_aluno)

  return novo_aluno


@router.get("/", response_model=List[AlunoResponse])
def listar_alunos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  alunos = db.query(Aluno).offset(skip).limit(limit).all()
  return alunos
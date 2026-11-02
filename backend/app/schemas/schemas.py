from datetime import date
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, EmailStr

class StatusMensalidadeEnum(str, Enum):
    PAGO = "PAGO"
    PENDENTE = "PENDENTE"
    ATRASADO = "ATRASADO"

class AlunoBase(BaseModel):
    nome: str
    data_nascimento: Optional[date] = None
    telefone: Optional[str] = None
    objetivo: Optional[str] = None
    observacoes_medicas: Optional[str] = None

class AlunoCreate(AlunoBase):
    email: EmailStr
    senha: str

class AlunoResponse(AlunoBase):
    id: int
    usuario_id: int
    class Config:
        from_attributes = True

class ExercicioBase(BaseModel):
    nome: str
    grupo_muscular: str
    url_video: Optional[str] = None

class ExercicioCreate(ExercicioBase):
    pass

class ExercicioResponse(ExercicioBase):
    id: int
    class Config:
        from_attributes = True

class ItemTreinoCreate(BaseModel):
    exercicio_id: int
    divisao: str
    series: int = 3
    repeticoes: str
    carga_kg: Optional[float] = None
    descanso_segundos: int = 60
    ordem: int = 1
    observacoes: Optional[str] = None

class ItemTreinoResponse(ItemTreinoCreate):
    id: int
    exercicio: ExercicioResponse
    class Config:
        from_attributes = True

class FichaTreinoCreate(BaseModel):
    aluno_id: int
    titulo: str
    descricao: Optional[str] = None
    itens: List[ItemTreinoCreate]

class FichaTreinoResponse(BaseModel):
    id: int
    aluno_id: int
    titulo: str
    descricao: Optional[str] = None
    ativa: bool
    itens: List[ItemTreinoResponse] = []
    class Config:
        from_attributes = True

class AvaliacaoFisicaCreate(BaseModel):
    aluno_id: int
    data_avaliacao: Optional[date] = None
    peso_kg: float
    altura_cm: Optional[float] = None
    percentual_gordura: Optional[float] = None
    medidas_json: Optional[Dict[str, Any]] = None
    observacoes: Optional[str] = None

class AvaliacaoFisicaResponse(AvaliacaoFisicaCreate):
    id: int
    class Config:
        from_attributes = True


# --- MENSALIDADES ---
class MensalidadeBase(BaseModel):
  aluno_id: int
  data_vencimento: date
  valor: float
  status: StatusMensalidadeEnum = StatusMensalidadeEnum.PENDENTE
  data_pagamento: Optional[date] = None

class MensalidadeCreate(MensalidadeBase):
    pass

class MensalidadeUpdate(BaseModel):
    status: Optional[StatusMensalidadeEnum] = None
    data_pagamento: Optional[date] = None

class MensalidadeResponse(MensalidadeBase):
    id: int
    class Config:
        from_attributes = True

class StatusMensalidadeEnum(str, Enum):
  PAGO = "PAGO"
  PENDENTE = "PENDENTE"
  ATRASADO = "ATRASADO"

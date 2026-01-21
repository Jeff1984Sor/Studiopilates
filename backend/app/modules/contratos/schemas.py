from datetime import date
from pydantic import BaseModel
from app.shared.schemas import ORMModel


class ContratoCreate(BaseModel):
    aluno_id: int
    plano_id: int
    unidade_id: int
    tipo_plano_id: int | None = None
    profissional_id: int | None = None
    inicio: date
    fim: date | None = None
    status: str = "ativo"
    observacoes: str | None = None


class ContratoOut(ORMModel):
    id: int
    aluno_id: int
    plano_id: int
    unidade_id: int
    tipo_plano_id: int | None
    profissional_id: int | None
    inicio: date
    fim: date | None
    status: str
    observacoes: str | None

from pydantic import BaseModel
from app.shared.schemas import ORMModel


class EnderecoAlunoCreate(BaseModel):
    logradouro: str
    numero: str
    cep: str
    cidade: str
    bairro: str
    principal: bool = False


class EnderecoAlunoOut(ORMModel):
    id: int
    logradouro: str
    numero: str
    cep: str
    cidade: str
    bairro: str
    principal: bool


class AlunoCreate(BaseModel):
    nome: str
    cpf: str
    rg: str | None = None
    unidade_id: int
    termo_uso_id: int | None = None
    status: str = "ativo"
    observacoes: str | None = None


class AlunoOut(ORMModel):
    id: int
    nome: str
    cpf: str
    rg: str | None
    unidade_id: int
    termo_uso_id: int | None
    status: str
    observacoes: str | None
    enderecos: list[EnderecoAlunoOut] = []

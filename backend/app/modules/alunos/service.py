from fastapi import HTTPException, status

from app.modules.alunos.repository import AlunoRepository, EnderecoRepository
from app.shared.utils import normalize_cpf
from app.modules.alunos.models import EnderecoAluno


class AlunoService:
    def __init__(self, repo: AlunoRepository, endereco_repo: EnderecoRepository):
        self.repo = repo
        self.endereco_repo = endereco_repo

    def create(self, data: dict):
        data["cpf"] = normalize_cpf(data["cpf"])
        if self.repo.get_by_cpf(data["cpf"]):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="CPF already registered")
        return self.repo.create(data)

    def add_endereco(self, aluno_id: int, data: dict):
        if data.get("principal"):
            self._clear_principal(aluno_id)
        data["aluno_id"] = aluno_id
        return self.endereco_repo.create(data)

    def _clear_principal(self, aluno_id: int):
        items, _ = self.endereco_repo.list(filters=[EnderecoAluno.aluno_id == aluno_id])
        for item in items:
            if item.principal:
                self.endereco_repo.update(item, {"principal": False})

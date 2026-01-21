from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.modules.alunos.schemas import AlunoCreate, AlunoOut, EnderecoAlunoCreate, EnderecoAlunoOut
from app.modules.alunos.repository import AlunoRepository, EnderecoRepository
from app.modules.alunos.service import AlunoService
from app.shared.pagination import Page, PageMeta

router = APIRouter(prefix="/alunos", tags=["alunos"])


@router.post("", response_model=AlunoOut)
def create_aluno(payload: AlunoCreate, db: Session = Depends(get_db)):
    service = AlunoService(AlunoRepository(db), EnderecoRepository(db))
    return service.create(payload.model_dump())


@router.get("/{aluno_id}", response_model=AlunoOut)
def get_aluno(aluno_id: int, db: Session = Depends(get_db)):
    repo = AlunoRepository(db)
    return repo.get(aluno_id)


@router.get("", response_model=Page[AlunoOut])
def list_alunos(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    order_by: str | None = None,
    order_dir: str = "asc",
    status: str | None = None,
    db: Session = Depends(get_db),
):
    repo = AlunoRepository(db)
    filters = []
    if status:
        filters.append(repo.model.status == status)
    items, total = repo.list(filters=filters, order_by=order_by, order_dir=order_dir, offset=(page - 1) * page_size, limit=page_size)
    return Page(items=items, meta=PageMeta(page=page, page_size=page_size, total=total))


@router.post("/{aluno_id}/enderecos", response_model=EnderecoAlunoOut)
def add_endereco(aluno_id: int, payload: EnderecoAlunoCreate, db: Session = Depends(get_db)):
    service = AlunoService(AlunoRepository(db), EnderecoRepository(db))
    return service.add_endereco(aluno_id, payload.model_dump())

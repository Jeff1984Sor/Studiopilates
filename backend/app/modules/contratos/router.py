from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.modules.contratos.schemas import ContratoCreate, ContratoOut
from app.modules.contratos.repository import ContratoRepository
from app.modules.contratos.service import ContratoService
from app.shared.pagination import Page, PageMeta

router = APIRouter(prefix="/contratos", tags=["contratos"])


@router.post("", response_model=ContratoOut)
def create_contrato(payload: ContratoCreate, db: Session = Depends(get_db)):
    service = ContratoService(ContratoRepository(db))
    return service.repo.create(payload.model_dump())


@router.get("", response_model=Page[ContratoOut])
def list_contratos(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)):
    service = ContratoService(ContratoRepository(db))
    items, total = service.repo.list(offset=(page - 1) * page_size, limit=page_size)
    return Page(items=items, meta=PageMeta(page=page, page_size=page_size, total=total))

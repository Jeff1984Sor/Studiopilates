from sqlalchemy.orm import Session
from app.shared.repository import BaseRepository
from app.modules.termos.models import TermoUso


class TermoRepository(BaseRepository[TermoUso]):
    def __init__(self, db: Session):
        super().__init__(db, TermoUso)

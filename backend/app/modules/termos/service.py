from app.modules.termos.repository import TermoRepository


class TermoService:
    def __init__(self, repo: TermoRepository):
        self.repo = repo

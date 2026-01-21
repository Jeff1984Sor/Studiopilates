from app.modules.profissionais.repository import ProfissionalRepository


class ProfissionalService:
    def __init__(self, repo: ProfissionalRepository):
        self.repo = repo

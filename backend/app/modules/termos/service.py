from __future__ import annotations

import re
from datetime import date, datetime
from io import BytesIO
from typing import Any

import markdown
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.alunos.models import Aluno
from app.modules.contratos.models import Contrato
from app.modules.planos.models import Plano, TipoPlano, TipoServico
from app.modules.profissionais.models import Profissional
from app.modules.termos.repository import TermoRepository
from app.modules.unidades.models import Unidade

TERMO_VARIAVEIS = [
    {"key": "aluno.nome", "label": "Nome do aluno", "example": "Maria Silva"},
    {"key": "aluno.cpf", "label": "CPF do aluno", "example": "123.456.789-00"},
    {"key": "aluno.rg", "label": "RG do aluno", "example": "12.345.678-9"},
    {"key": "aluno.status", "label": "Status do aluno", "example": "ativo"},
    {"key": "aluno.criado_em", "label": "Data de cadastro do aluno", "example": "2025-01-12"},
    {"key": "unidade.nome", "label": "Nome da unidade", "example": "Centro"},
    {"key": "unidade.ocupacao_max", "label": "Ocupacao maxima da unidade", "example": "16"},
    {"key": "contrato.id", "label": "Codigo do contrato", "example": "245"},
    {"key": "contrato.inicio", "label": "Inicio do contrato", "example": "2025-02-01"},
    {"key": "contrato.fim", "label": "Fim do contrato", "example": "2025-08-01"},
    {"key": "contrato.status", "label": "Status do contrato", "example": "ativo"},
    {"key": "plano.descricao", "label": "Descricao do plano", "example": "Pilates 2x semana"},
    {"key": "plano.preco", "label": "Preco do plano", "example": "250.00"},
    {"key": "tipo_plano.descricao", "label": "Tipo do plano", "example": "Mensal"},
    {"key": "tipo_servico.descricao", "label": "Tipo de servico", "example": "Pilates"},
    {"key": "profissional.nome", "label": "Nome do profissional", "example": "Carla Souza"},
    {"key": "data_atual", "label": "Data atual", "example": "2026-01-21"},
]


class TermoService:
    def __init__(self, repo: TermoRepository):
        self.repo = repo


class TermoRenderer:
    def __init__(self, db: Session):
        self.db = db
        self.repo = TermoRepository(db)

    def variables(self) -> list[dict[str, str]]:
        return TERMO_VARIAVEIS

    def render(self, template: str, context: dict[str, Any]) -> str:
        pattern = re.compile(r"{{\s*([\w\.]+)\s*}}")

        def replace(match: re.Match[str]) -> str:
            key = match.group(1)
            value = self._resolve_key(context, key)
            return value if value is not None else match.group(0)

        return pattern.sub(replace, template)

    def build_context(self, aluno_id: int, contrato_id: int | None = None) -> dict[str, Any]:
        aluno = self.db.get(Aluno, aluno_id)
        if not aluno:
            return {}

        unidade = self.db.get(Unidade, aluno.unidade_id) if aluno.unidade_id else None
        contrato = self._get_contrato(aluno_id, contrato_id)
        plano = self.db.get(Plano, contrato.plano_id) if contrato and contrato.plano_id else None
        tipo_plano = self.db.get(TipoPlano, plano.tipo_plano_id) if plano else None
        tipo_servico = self.db.get(TipoServico, plano.tipo_servico_id) if plano else None
        profissional = self.db.get(Profissional, contrato.profissional_id) if contrato and contrato.profissional_id else None

        return {
            "aluno": {
                "nome": aluno.nome,
                "cpf": aluno.cpf,
                "rg": aluno.rg,
                "status": aluno.status,
                "criado_em": self._format_date(aluno.criado_em),
            },
            "unidade": {
                "nome": unidade.nome if unidade else "",
                "ocupacao_max": unidade.ocupacao_max if unidade else "",
            },
            "contrato": {
                "id": contrato.id if contrato else "",
                "inicio": self._format_date(contrato.inicio) if contrato else "",
                "fim": self._format_date(contrato.fim) if contrato else "",
                "status": contrato.status if contrato else "",
            },
            "plano": {
                "descricao": plano.descricao if plano else "",
                "preco": f"{plano.preco:.2f}" if plano and plano.preco is not None else "",
            },
            "tipo_plano": {"descricao": tipo_plano.descricao if tipo_plano else ""},
            "tipo_servico": {"descricao": tipo_servico.descricao if tipo_servico else ""},
            "profissional": {"nome": profissional.nome if profissional else ""},
            "data_atual": date.today().isoformat(),
        }

    def generate_pdf(self, text: str) -> bytes:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        body = []
        html = markdown.markdown(text)
        blocks = [b.strip() for b in html.split("</p>") if b.strip()]
        for block in blocks:
            cleaned = block.replace("<p>", "").strip()
            if not cleaned:
                continue
            body.append(Paragraph(cleaned, styles["Normal"]))
            body.append(Spacer(1, 12))
        if not body:
            body = [Paragraph("Termo de uso", styles["Normal"])]
        doc.build(body)
        return buffer.getvalue()

    def _get_contrato(self, aluno_id: int, contrato_id: int | None) -> Contrato | None:
        if contrato_id:
            return self.db.get(Contrato, contrato_id)
        stmt = (
            select(Contrato)
            .where(Contrato.aluno_id == aluno_id)
            .order_by(Contrato.criado_em.desc())
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def _format_date(self, value: date | datetime | None) -> str:
        if not value:
            return ""
        if isinstance(value, datetime):
            return value.date().isoformat()
        return value.isoformat()

    def _resolve_key(self, context: dict[str, Any], key: str) -> str | None:
        if key in context and not isinstance(context[key], dict):
            return self._stringify(context[key])
        current: Any = context
        for part in key.split("."):
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        return self._stringify(current)

    def _stringify(self, value: Any) -> str:
        if value is None:
            return ""
        return str(value)

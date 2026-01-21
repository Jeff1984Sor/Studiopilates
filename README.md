# StudioPilates

Sistema completo para Studio de Pilates (API-first) com FastAPI + Next.js.

## Requisitos
- Docker + Docker Compose
- Python 3.11+ (opcional para rodar local sem Docker)
- Node 20+ (opcional para rodar local sem Docker)

## Subir tudo com Docker
1. `docker compose up --build`
2. A API sobe em `http://localhost:8000`
3. Swagger em `http://localhost:8000/docs`
4. Frontend em `http://localhost:3000`

## Variaveis de ambiente
- Backend: copie `backend/.env.example` para `backend/.env`
- Frontend: copie `frontend/.env.example` para `frontend/.env`

## Migrations
- DEV (SQLite):
  - Ajuste `backend/.env` com `DATABASE_URL=sqlite:///./studiopilates.db`
  - `cd backend`
  - `alembic upgrade head`

- PROD (Postgres):
  - Ajuste `DATABASE_URL=postgresql+psycopg://user:pass@host:5432/studiopilates`
  - `cd backend`
  - `alembic upgrade head`

## Seed admin
- `cd backend`
- `python scripts/seed_admin.py`

## Observabilidade
- Logs com `request_id` em cada request (header `X-Request-ID` opcional).

## Sugestoes de melhoria
- Indices adicionais para buscas frequentes (por data, status, unidade).
- FKs com `ondelete` adequados para historico e auditoria.
- Particionamento de agenda e financeiro por periodo quando crescer.
- Job scheduler para lembretes por WhatsApp (APScheduler/Celery).

## Estrutura
- `backend/` FastAPI + SQLAlchemy + Alembic
- `frontend/` Next.js App Router + Tailwind + shadcn/ui

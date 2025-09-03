import os
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# ================================

# Pega a URL do banco do Fly
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL não definida nos secrets do Fly!")

# Ajusta o prefixo para asyncpg
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

# Log seguro (não mostra usuário e senha)
safe_url = DATABASE_URL.replace(DATABASE_URL.split("@")[0], "****")
print("DATABASE_URL segura:", safe_url)

SCHEMA = "backend"
Base = declarative_base()

# ================================
# ENGINE E SESSÃO ASYNC
# ================================

engine = create_async_engine(DATABASE_URL, future=True, echo=False)
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

# ================================
# CRIAÇÃO DO SCHEMA E TABELAS
# ================================

async def create_db(schema: str = SCHEMA):
    """
    Cria o schema e todas as tabelas definidas nos models.
    """
    async with engine.begin() as conn:
        # Cria schema se não existir
        await conn.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
        # Cria tabelas dentro do schema
        await conn.run_sync(Base.metadata.create_all, schema=schema)
    print(f"Schema '{schema}' e tabelas criadas com sucesso!")

# ================================
# GERENCIAMENTO DE SESSÃO
# ================================

class DBSession:
    """
    Context manager para usar sessões async SQLAlchemy.
    """

    def __init__(self):
        self.session = async_session()

    async def __aenter__(self):
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

async def get_db():
    """
    Retorna uma sessão async para ser usada em rotas FastAPI.
    """
    return DBSession()

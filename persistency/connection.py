from config import Config
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Loading config to get database_url
DATABASE_URL = Config.DATABASE_URL
SCHEMA = "backend"
Base = declarative_base()

# Creating one async connection to database
engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(
    bind=engine, autocommit=False, autoflush=False, class_=AsyncSession
)

def create_db(schema=SCHEMA):
    Base.metadata.create_all(bind=engine, schema=schema)


class DBSession:
    def __init__(self):
        self.session = async_session()

    async def __aenter__(self):
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()


async def get_db():
    return DBSession()

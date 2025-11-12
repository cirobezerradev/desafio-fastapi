from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

DATABASE_URL = 'postgresql+asyncpg://postgres:postgres@localhost:5432/workout_db'

engine = create_async_engine(DATABASE_URL)

async_session = async_sessionmaker(engine, expire_on_commit=False, autocommit=False, autoflush=False)


async def get_session():
    async with async_session() as session:
        yield session

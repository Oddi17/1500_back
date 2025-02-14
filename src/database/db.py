from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import settings

engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg, #строка для подключения к БД
    echo=True, #выводит в консоль все запросы их алхимии к БД
    # poll_size=5, #количество подключения к БД
    # max_overflow=10,#дополнительный подключения, если все 5 предыдущих заняты
)

async_session = async_sessionmaker(engine,expire_on_commit=False)


# async def select_version():
#     async with engine.connect() as conn:
#         res = await conn.execute(text("SELECT VERSION()"))
#         version = res.scalar()
#         print(f"Database version: {version}")
 
 
# asyncio.run(select_version())


class Base(DeclarativeBase):
    pass


async def get_async_session():
    async with async_session() as session:
        yield session
        # try:
        #     yield session
        # finally:
        #     await session.close()




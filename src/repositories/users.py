from sqlalchemy import select
from models.users import Users
from utils.repository import SQLAlchemyRepository
from database.db import async_session

class UsersRepository():
    model = Users
    
    @classmethod
    async def get_user_by_login(cls,login):
        async with async_session() as session:
            stmt = select(cls.model).filter_by(login=login)
            user = await session.execute(stmt)
            return user.scalar_one_or_none()
        
    @classmethod
    async def get_user_by_id(cls,id):
        async with async_session() as session:
            stmt = select(cls.model).filter_by(id=id)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

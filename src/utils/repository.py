from abc import ABC, abstractmethod
from fastapi import Depends
from database.db import async_session
from database.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, update

class AbstractRepository(ABC):

   
    
    @abstractmethod
    async def delete():
        raise NotImplemented

    @abstractmethod
    async def add():
        raise NotImplemented
    
    @abstractmethod
    async def get_all():
        raise NotImplemented
    
    @abstractmethod
    async def get_single():
        raise NotImplemented
    

    

class SQLAlchemyRepository(AbstractRepository):
    model = None

    # def __init__(self, session:AsyncSession = Depends(get_async_session)):
    #     self.session = session

    # async def get_all(self):
    #     async with async_session() as session:
    #         stmt = select(self.model).filter(self.model.valid == 't')
    #         res = await session.execute(stmt)
    #         # res = res.scalars().all()
    #         # print(res.scalars().all())
    #         res = [row.to_read_model() for row in res.scalars().all()]
    #         # print(res[0].to_read_model())
    #         return res[1]

    async def add(self, data:dict)->int:
        async with async_session() as session:  
            instance = self.model(**data)  
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance.id
    
    async def get_all(self,*filters):
        async with async_session() as session:
            stmt = select(self.model)
            if filters:
                stmt = stmt.filter(*filters).order_by(self.model.recdt)
            res = await session.execute(stmt)
            res = [row.to_read_model() for row in res.scalars().all()]
            return res

    async def get_single(self,*filters):
        async with async_session() as session:
            stmt = select(self.model).filter(*filters)
            res = await session.execute(stmt)
            res = res.scalar_one_or_none()
            if res:
                res.to_read_model()
            return res
        
    async def delete(self,*filters):
        async with async_session() as session:
            if filters:
                stmt = delete(self.model).where(*filters)
                res = await session.execute(stmt)
                await session.commit()
                return res.rowcount
            return None
        
    async def get_all_users(self,*filters):
        async with async_session() as session:
            stmt = select(self.model)
            if filters:
                stmt = stmt.filter(*filters).order_by(self.model.id)
            res = await session.execute(stmt)
            res = [row.to_read_model() for row in res.scalars().all()]
            return res
    async def change(self,id:int,data:dict):
        async with async_session() as session:
            stmt = (
                    update(self.model)
                    .where(self.model.id == id)
                    .values(**data)
                )
            res = await session.execute(stmt)
            await session.commit()
            #return res.scalars().first()





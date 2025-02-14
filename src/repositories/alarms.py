from models.alarms import Alarms
from utils.repository import SQLAlchemyRepository
from sqlalchemy import select,and_
from database.db import async_session

class AlarmsRepository(SQLAlchemyRepository):
    model = Alarms

    @classmethod
    async def get_start_alarm(cls,start_unix,sid):
        async with async_session() as session:
            # Подзапрос: найти первую запись со status = False
            first_false_subquery = (
                select(cls.model.id)
                .where(and_(
                            cls.model.sid == sid,
                            cls.model.status == False,
                            cls.model.recdt < start_unix,
                            ))
                .order_by(cls.model.id)
                .limit(1)
                .scalar_subquery()
            )

            # Основной запрос: найти первую запись со status = True после найденного False
            next_true_query = (
                select(cls.model)
                .where(and_(cls.model.status == True, 
                            cls.model.id > first_false_subquery))
                .order_by(cls.model.id)
                .limit(1)
            )
            res = await session.execute(next_true_query)
            res = res.scalar_one_or_none()
            if res:
                res = res.to_read_model()
            return res
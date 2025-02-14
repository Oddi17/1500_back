from utils.repository import AbstractRepository
from datetime import datetime, timedelta
from sqlalchemy import and_

class AnaliticControleService():
    def __init__(self, analitic_control_repo: type[AbstractRepository]):
        self.analitic_control_repo = analitic_control_repo()

    async def send_data(self,data):
        res = await self.analitic_control_repo.add(data)
        return res
        
    async def get_data(self,start_time,end_time):
        filters = []
        if start_time and end_time:
            start_time = datetime.fromisoformat(start_time)
            end_time = datetime.fromisoformat(end_time)
            start_time = start_time.replace(tzinfo=None)
            end_time = end_time.replace(tzinfo=None)
            filters.append(and_(
                self.analitic_control_repo.model.recdt >= start_time,
                self.analitic_control_repo.model.recdt <= end_time
            ))
        res = await self.analitic_control_repo.get_all(*filters)
        for item in res:
            item.recdt = (item.recdt + timedelta(hours=3))
        return res
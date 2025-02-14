from schemas.alarms import AlarmsSchema
from utils.repository import AbstractRepository
from sqlalchemy import and_
from datetime import datetime,timezone,timedelta
from repositories.alarms import AlarmsRepository


class AlarmsService:
    def __init__(self, alarms_repo: type[AbstractRepository]):
        self.alarms_repo = alarms_repo()

    def grouped_data(self,data):
        grouped_data = {}
        for device in data:
            if device.sid not in grouped_data:
                grouped_data[device.sid] = []
            grouped_data[device.sid].append(device)
        return grouped_data
    
    async def get_reliability(self,start_time,end_time):
            sids = ["VOS1_IDLESTATION","VOS1_NOPOWER"]
            filters = [
                self.alarms_repo.model.sid.in_(sids),
            ]
            if start_time and end_time:
                start_time_dt = datetime.fromisoformat(start_time)
                end_time_dt = datetime.fromisoformat(end_time)
                st_unix = int(start_time_dt.timestamp())
                et_unix = int(end_time_dt.timestamp())
                filters.append(and_(
                    self.alarms_repo.model.recdt >= st_unix,
                    self.alarms_repo.model.recdt <= et_unix
                ))
            else:
                return None
            alarms = await self.alarms_repo.get_all(*filters)
            grouped_alarms = self.grouped_data(alarms)
            
            for item in grouped_alarms:
                if grouped_alarms[item][0].status == True:
                    start_status_alarm = await AlarmsRepository.get_start_alarm(st_unix,item)
                    if start_status_alarm:
                        grouped_alarms[item].insert(0,start_status_alarm)

                if grouped_alarms[item][-1].status == True:
                    filters_end_status = [
                        self.alarms_repo.model.sid == item,
                        self.alarms_repo.model.recdt > et_unix,
                        self.alarms_repo.model.status == False,
                    ] 
                    end_status_alarm = await self.alarms_repo.get_single(*filters_end_status)
                    if end_status_alarm:
                        grouped_alarms[item].append(end_status_alarm)
                    else:
                        grouped_alarms[item].append(AlarmsSchema(
                                                        id=grouped_alarms[item][-1].id + 1,
                                                        recdt="До настоящего времени",
                                                        sid=grouped_alarms[item][-1].sid,
                                                        alarmname=grouped_alarms[item][-1].alarmname,
                                                        abname=grouped_alarms[item][-1].abname,
                                                        status=grouped_alarms[item][-1].status
                                                    ))
            result = []
            for item in grouped_alarms:
                start_point = None
                end_point = None
                for alarm in grouped_alarms[item]:
                    if alarm.status == True and not start_point:
                        start_point = alarm
                    if alarm.status == False and start_point:
                        end_point = alarm
                    if start_point and end_point:
                        start_time = (datetime.fromtimestamp((start_point.recdt),tz=timezone.utc) + timedelta(hours=3)).strftime('%d-%m-%Y %H:%M:%S')
                        if end_point.recdt == "До настоящего времени":
                            end_time = "До настоящего времени"
                            current_unix_time = int(datetime.now(timezone.utc).timestamp())
                            duration = current_unix_time - start_point.recdt
                            formatted_duration = str(timedelta(seconds=duration))
                        else:
                            end_time = (datetime.fromtimestamp((end_point.recdt),tz=timezone.utc) + timedelta(hours=3)).strftime('%d-%m-%Y %H:%M:%S')
                            duration = end_point.recdt - start_point.recdt
                            formatted_duration = str(timedelta(seconds=duration))
                        result.append({
                                        "name":start_point.alarmname,
                                        "range":f"{start_time} - {end_time}",
                                        "area":start_point.abname,
                                        "duration":formatted_duration
                                        })
            return result
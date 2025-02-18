from utils.repository import AbstractRepository
from sqlalchemy import and_
from services.devices_core import DevicesCore
from datetime import datetime
from collections import defaultdict

class DevicesService:
    def __init__(self, devices_repo: type[AbstractRepository]):
        self.devices_repo = devices_repo()
        self.devices_core = DevicesCore()
    
    async def get_devices(self,start_time,end_time,sample):
        sids = ["VOS1_VIN","VOS1_VV1_PROD","VOS1_VV2_PROD","VOS1_V_WASHF","VOS1_V_SLG_OS1","VOS1_V_SLG_OS2","VOS1_VGPV_E1"]
        filters = [
            self.devices_repo.model.sid.in_(sids),
            self.devices_repo.model.valid == 't'
        ]
        if start_time and end_time:
            start_time_dt = datetime.fromisoformat(start_time)
            end_time_dt = datetime.fromisoformat(end_time)
            st_unix = int(start_time_dt.timestamp())
            et_unix = int(end_time_dt.timestamp())
            filters.append(and_(
                self.devices_repo.model.recdt >= st_unix,
                self.devices_repo.model.recdt <= et_unix
            ))
        devices = await self.devices_repo.get_all(*filters)
        grouped_data = self.devices_core.grouped_data(devices)
        data_diff = []
        for key,array in grouped_data.items():
            diff_data_device = self.devices_core.difference_value(array,sample)
            data_diff.append({"sid":key,"devices_values":diff_data_device})
        # print(*data_diff,sep="\n")
        summ_array = []
        summ_dict = {}
        summ_dict['dif_date_time'] = 'Итого'
        for item in data_diff:
            summ = self.devices_core.summ_values(item['devices_values'])
            summ_dict[item['sid']] = summ
        summ_array.append(summ_dict)
        grouped_data = defaultdict(dict)    
        for item in data_diff:
            sid = item["sid"]  
            for value in item["devices_values"]:
                date_time = value["dif_date_time"]
                grouped_data[date_time]["dif_date_time"] = date_time
                grouped_data[date_time][sid] = value["dif_value"]
        data_source = [{**v} for _, v in grouped_data.items()]
        return {"data_source":data_source,"summ":summ_array}
    

    async def get_chemistry(self,start_time,end_time,sample):
        sids = ["VOS1_VIN","VOS1_V_KOAG_SUM","VOS1_V_FLOK_SUM","VOS1_V_GHN_SUM","Сoefficient"]
        filters = [
            self.devices_repo.model.sid.in_(sids),
            self.devices_repo.model.valid == 't'
        ]
        if start_time and end_time:
            start_time_dt = datetime.fromisoformat(start_time)
            end_time_dt = datetime.fromisoformat(end_time)
            st_unix = int(start_time_dt.timestamp())
            et_unix = int(end_time_dt.timestamp())
            filters.append(and_(
                self.devices_repo.model.recdt >= st_unix,
                self.devices_repo.model.recdt <= et_unix
            ))
        devices = await self.devices_repo.get_all(*filters)
        grouped_data = self.devices_core.grouped_data(devices)
        diff_data_flok = []
        for key,array in grouped_data.items():
            if key == "VOS1_V_FLOK_SUM" or key == "VOS1_VIN" or key == "Сoefficient":
                diff_data_device = self.devices_core.difference_value(array,sample)
                diff_data_flok.append({"sid":key,"devices_values":diff_data_device})
        flok_data = defaultdict(dict)    
        for item in diff_data_flok:
                sid = item["sid"]
                for value in item["devices_values"]:
                    date_time = value["dif_date_time"]
                    flok_data[date_time]["dif_date_time"] = date_time
                    if value["dif_value"] != "Отсутствуют данные":
                        rash_value = round(value["dif_value"],4)
                    else:
                        rash_value = value["dif_value"]
                    flok_data[date_time][sid] = rash_value
        for item in flok_data:
            if 'Сoefficient' in flok_data[item]:
                if flok_data[item]['Сoefficient'] != 'Отсутствуют данные':
                    p = item['Сoefficient']
            else:
                p = 2.4
            if flok_data[item]['VOS1_VIN'] == 0: #or flok_data[item]['VOS1_V_FLOK_SUM'] == "Отсутствуют данные":
                 flok_data[item]["Udel"] = 0
            elif flok_data[item]['VOS1_V_FLOK_SUM'] == "Отсутствуют данные":
                 flok_data[item]["Udel"] = "Отсутствуют данные"   
            else:         
                flok_data[item]["Udel"] = round(((flok_data[item]['VOS1_V_FLOK_SUM'])*p)/((flok_data[item]['VOS1_VIN'])/1000),4)
        result = self.devices_core.chemistry_values(grouped_data)
        values = list(flok_data.values())
        if values:
            result['VOS1_V_FLOK_SUM'] = values
        return result
    
    async def get_electricity(self,start_time,end_time):
        sids = ["VOS1_VIN","VOS1_WSUM"]
        filters = [
            self.devices_repo.model.sid.in_(sids),
            self.devices_repo.model.valid == 't'
        ]
        if start_time and end_time:
            start_time_dt = datetime.fromisoformat(start_time)
            end_time_dt = datetime.fromisoformat(end_time)
            st_unix = int(start_time_dt.timestamp())
            et_unix = int(end_time_dt.timestamp())
            filters.append(and_(
                self.devices_repo.model.recdt >= st_unix,
                self.devices_repo.model.recdt <= et_unix
            ))
        devices = await self.devices_repo.get_all(*filters)
        grouped_data = self.devices_core.grouped_data(devices)
        result = self.devices_core.electricity_values(grouped_data)  
        return result
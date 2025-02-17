from datetime import datetime,timezone,timedelta
from dateutil.relativedelta import relativedelta

class DevicesCore:
    def grouped_data(self,data):
        grouped_data = {}
        for device in data:
            if device.sid not in grouped_data:
                grouped_data[device.sid] = []
            grouped_data[device.sid].append(device)
        return grouped_data

    def summ_values(self,array_object_data):
        summa = 0
        for item in array_object_data:
            if item['dif_value'] != 'Отсутствуют данные':
                summa = summa + item['dif_value']
        return summa   

    def difference_value(self,data=None,sample="1_hour"):
        if data is None:
            raise ValueError("Данные не предоставлены")
        sample_to_dif_time = {
            "1_hour": [1,timedelta(hours=1),timedelta(hours=1,minutes=2)],
            "2_hour": [2,timedelta(hours=2),timedelta(hours=2,minutes=2)],
            "day": [24,timedelta(days=1),timedelta(days=1,minutes=2)],
            "month": [30*24,relativedelta(months=1), timedelta(days=1)],  # Примерное количество часов в месяце
        }
        if sample in sample_to_dif_time:
            delta = sample_to_dif_time.get(sample) 
        else:
            raise KeyError(f"Ключ '{sample}' отсутствует в словаре sample_to_dif_time")
        new_data = []
        for device in data:
            device.recdt = datetime.fromtimestamp((device.recdt),tz=timezone.utc).replace(second=0,microsecond=0) #ошибка тута!!!!!!!!!!!!!!!!!!!!!!!!!! преобразование воемени
            new_data.append(device)

        sorted_data = sorted(new_data, key=lambda x: x.recdt)
        filtered_data = [sorted_data[0]]  
        current = sorted_data[0]
        next_interval = current.recdt + delta[1]
        
        if sample == "day":
            for item in sorted_data[1:]:
                if item.recdt > current.recdt and item.recdt < next_interval:
                    current = item
                if item.recdt >= next_interval:
                    filtered_data.append(current)
                    current = item
                    next_interval = current.recdt + delta[1]         
            if current not in filtered_data:
                filtered_data.append(current)
        elif sample == "month":
            for item in sorted_data[1:]:
                if item.recdt > current.recdt and item.recdt < next_interval:
                    current = item
                if item.recdt >= next_interval:
                    filtered_data.append(current)
                    current = item
                    next_interval = current.recdt + delta[1]
        else:
            for item in sorted_data[1:]:
                if delta[1] <= (item.recdt - current.recdt) <= delta[2]:
                    filtered_data.append(item)
                    current = item
                    next_interval = current.recdt + delta[1]
                else:
                    # Добавляем пропущенные интервалы
                    while item.recdt > next_interval:
                        filtered_data.append({"value":"Нет данных","recdt":next_interval})
                        next_interval += delta[1]
                    # Проверяем текущий элемент после добавления пропусков
                    # if next_interval - delta[2] <= item.recdt <= next_interval:
                    if next_interval - timedelta(minutes=2) <= item.recdt <= next_interval + timedelta(minutes=2):    
                        filtered_data.append(item)
                        current = item
                        next_interval = current.recdt + delta[1]       
        # print(*filtered_data,sep="\n")
        difference_array = [] 
        for i in range(0,len(filtered_data)-1):
                if type(filtered_data[i]) is dict and type(filtered_data[i+1]) is dict:
                    dif_value = "Отсутствуют данные"
                    item_date_1 = filtered_data[i]["recdt"]
                    item_date_2 = filtered_data[i+1]["recdt"]
                    dif_date_time = f"{(item_date_1 + timedelta(hours=3)).strftime('%d-%m-%Y %H:%M')}-{(item_date_2 + timedelta(hours=3)).strftime('%d-%m-%Y %H:%M')}"
                elif type(filtered_data[i]) is dict:
                    dif_value = "Отсутствуют данные"
                    item_date = filtered_data[i]["recdt"]
                    dif_date_time = f"{(item_date + timedelta(hours=3)).strftime('%d-%m-%Y %H:%M')}-{(filtered_data[i+1].recdt + timedelta(hours=3)).strftime('%d-%m-%Y %H:%M')}"
                elif type(filtered_data[i+1]) is dict:
                    dif_value = "Отсутствуют данные"
                    item_date = filtered_data[i+1]["recdt"]
                    dif_date_time = f"{(filtered_data[i].recdt + timedelta(hours=3)).strftime('%d-%m-%Y %H:%M')}-{(item_date + timedelta(hours=3)).strftime('%d-%m-%Y %H:%M')}"

                else:
                    if filtered_data[i].sid == "Coefficient":
                        dif_value = filtered_data[i].paramvalue
                        dif_date_time = f"{(filtered_data[i].recdt + timedelta(hours=3)).strftime('%d-%m-%Y %H:%M')} - {(filtered_data[i+1].recdt + timedelta(hours=3)).strftime('%d-%m-%Y %H:%M')}"
                    else:
                        dif_value = filtered_data[i+1].paramvalue-filtered_data[i].paramvalue
                        dif_date_time = f"{(filtered_data[i].recdt + timedelta(hours=3)).strftime('%d-%m-%Y %H:%M')} - {(filtered_data[i+1].recdt + timedelta(hours=3)).strftime('%d-%m-%Y %H:%M')}"
                difference_array.append({'dif_date_time':dif_date_time, "dif_value":dif_value})
        return difference_array 
    
    def chemistry_values(self,data):
        p = {
            "VOS1_V_KOAG_SUM":1280,
            "VOS1_V_GHN_SUM":1265,
            } 
        chem_dict = {}
        for key,value in data.items():
            chem_value = (value[-1].paramvalue - value[0].paramvalue)
            chem_dict[key]=chem_value
        res_dict = {}
        for key,value in chem_dict.items():
            if key != "VOS1_VIN" and key != "VOS1_V_FLOK_SUM":
                chem_out_value = ((value*p[key])/((chem_dict["VOS1_VIN"])/1000))
                res_dict[key] = {"sid":key,"volume":chem_dict["VOS1_VIN"],"consumption":round(value,4),"res_value":round(chem_out_value,4)}
        return res_dict
    
    def electricity_values(self,data):
        elect_dict = {}
        for key,value in data.items():
            elect_value = (value[-1].paramvalue - value[0].paramvalue)
            if elect_value < 0:
                elect_value = 0
            elect_dict[key]=elect_value
        res_dict = {}
        for key,value in elect_dict.items():
            if key != "VOS1_VIN":
                elec_out_value = value/elect_dict["VOS1_VIN"] # /1000???
                res_dict[key] = {"sid":key,"volume":elect_dict["VOS1_VIN"],"consumption":round(value,4),"res_value":round(elec_out_value,4)}
        return res_dict
from pydantic import BaseModel, ConfigDict
from datetime import datetime,timezone,timedelta
from dateutil.relativedelta import relativedelta




def grouped_data(data):
    grouped_data = {}
    for device in data:
        if device.sid not in grouped_data:
            grouped_data[device.sid] = []
        grouped_data[device.sid].append(device)
    return grouped_data
    # Результат
    # for sid, devices in grouped_data.items():
    #     print(f"Device {sid}:")
    #     for device in devices:
    #         print(f"  - {device.param_name}: {device.param_value} {device.unit}")
    # pass


def difference_value(data=None,sample="1_hour"):
    if data is None:
        raise ValueError("Данные не предоставлены")
    sample_to_dif_time = {
        "1_hour": [1,timedelta(hours=1)],
        "2_hour": [2,timedelta(hours=2)],
        "day": [24,timedelta(days=1)],
        "month": [30*24,timedelta(days=30)],  # Примерное количество часов в месяце
    }
    if sample in sample_to_dif_time:
        delta = sample_to_dif_time.get(sample)
    else:
        raise KeyError(f"Ключ '{sample}' отсутствует в словаре sample_to_dif_time")
    last_data = [
            {
                "date_time":datetime.fromtimestamp((entry.recdt),tz=timezone.utc).replace(tzinfo=None,second=0,microsecond=0),
                "value":entry.param_value
            } for entry in data
        ]  
    last_data.sort(key=lambda x: x['date_time'])
    list_difference = []
    sig = False
    excepted_next = last_data[0]["date_time"]
    for i in range(0,len(last_data)-1):
        if i+delta[0] < len(last_data):
            
            if last_data[i]["date_time"] == excepted_next:
                sig = False
            else:
                excepted_next = excepted_next + delta[1]    

            if not sig:
                print("zashel")
                expected_time = last_data[i]['date_time'] + delta[1]
                actual_time = last_data[i + delta[0]]['date_time']
                print(expected_time,actual_time)
                if expected_time == actual_time:
                    value = last_data[i+delta[0]]['value'] - last_data[i]['value']
                    date_time = f"{last_data[i]['date_time'].strftime('%Y-%m-%d %H:%M')}-{last_data[i+delta[0]]['date_time'].strftime('%Y-%m-%d %H:%M')}"
                    list_difference.append({'date_time':date_time, "value":value})
                else:
                    excepted_next = expected_time + delta[1]
                    sig = True
                    value = "Ошибка в данных"
                    date_time = f"{last_data[i]['date_time'].strftime('%Y-%m-%d %H:%M')}-{expected_time.strftime('%Y-%m-%d %H:%M')}"
                    list_difference.append({'date_time':date_time, "value":value})
    # print(*list_difference, sep='\n')
    return list_difference  


  





    # filtered_data = []
    # filtered_data.append(sorted_data[0])
    # current_item = sorted_data[0]
    # expected_date_1 = current_item.recdt + delta[1]
    # expected_date_2 = current_item.recdt + delta[2]
    # for i in range(0,len(sorted_data)-1):
    #     if delta[1] <= sorted_data[i].recdt-current_item.recdt <= delta[2]:
    #         filtered_data.append(sorted_data[i])
    #         current_item = sorted_data[i]
    #         expected_date_1 = current_item.recdt + delta[1]
    #         expected_date_2 = current_item.recdt + delta[2]
    #     else:
    #         if sorted_data[i].recdt > expected_date_1:
    #         #    filtered_data.append(f"Нет данных за {expected_date_1.strftime('%Y-%m-%d %H:%M')}")
    #            filtered_data.append({"value":"Нет данных","recdt":expected_date_1})
    #         #    print(f"Нет данных за {expected_date_1.strftime('%Y-%m-%d %H:%M')}")
    #            expected_date_1 = expected_date_1 + delta[1]
    #            expected_date_2 = expected_date_1 + timedelta(minutes=2)
    #         if expected_date_1 <= sorted_data[i].recdt <= expected_date_2:
    #             current_item = sorted_data[i]
    #             filtered_data.append(current_item)
    #             expected_date_1 = expected_date_1 + delta[1]
    #             expected_date_2 = expected_date_1 + timedelta(minutes=2)
def difference_value_another(data=None,sample="1_hour"):
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
        device.recdt = datetime.fromtimestamp((device.recdt),tz=timezone.utc).replace(tzinfo=None,second=0,microsecond=0)
        new_data.append(device)

    sorted_data = sorted(new_data, key=lambda x: x.recdt)
    filtered_data = [sorted_data[0]]  
    current = sorted_data[0]
    next_interval = current.recdt + delta[1]

    for item in sorted_data[1:]:
        if sample == "month":
            expected_date = current.recdt + delta[1]
            lower_bound = expected_date - delta[2]
            upper_bound = expected_date + delta[2]
            
            if lower_bound <= item.recdt <= upper_bound:
                filtered_data.append(item)
                current = item
                next_interval = current.recdt + delta[1]
        else:
            if delta[1] <= (item.recdt - current.recdt) <= delta[2]:
                filtered_data.append(item)
                current = item
                next_interval = current.recdt + delta[1]
            else:
                # Добавляем пропущенные интервалы
                while item.recdt > next_interval:
                    filtered_data.append({"value":"Нет данных","recdt":next_interval})
                    # print(f"Нет данных за {next_interval.strftime('%Y-%m-%d %H:%M')}")
                    # filtered_data.append(f"Нет данных за {next_interval.strftime('%Y-%m-%d %H:%M')}")
                    next_interval += delta[1]
                
                # Проверяем текущий элемент после добавления пропусков
                # if next_interval - delta[2] <= item.recdt <= next_interval:
                if next_interval - timedelta(minutes=2) <= item.recdt <= next_interval + timedelta(minutes=2) :    
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
                 dif_date_time = f"{item_date_1.strftime('%Y-%m-%d %H:%M')}-{item_date_2.strftime('%Y-%m-%d %H:%M')}"
            elif type(filtered_data[i]) is dict:
                dif_value = "Отсутствуют данные"
                item_date = filtered_data[i]["recdt"]
                dif_date_time = f"{item_date.strftime('%Y-%m-%d %H:%M')}-{filtered_data[i+1].recdt.strftime('%Y-%m-%d %H:%M')}"
            elif type(filtered_data[i+1]) is dict:
                dif_value = "Отсутствуют данные"
                item_date = filtered_data[i+1]["recdt"]
                dif_date_time = f"{filtered_data[i].recdt.strftime('%Y-%m-%d %H:%M')}-{item_date.strftime('%Y-%m-%d %H:%M')}"
            else:
                dif_value = filtered_data[i+1].param_value-filtered_data[i].param_value
                dif_date_time = f"{filtered_data[i].recdt.strftime('%Y-%m-%d %H:%M')}-{filtered_data[i+1].recdt.strftime('%Y-%m-%d %H:%M')}"
            
            difference_array.append({'dif_date_time':dif_date_time, "dif_value":dif_value})
    # print(*difference_array,sep="\n")     
    return difference_array          
            
            

def summ_values(array_object_data):
    summa = 0
    for item in array_object_data:
        summa = summa + item['dif_value']
    return summa
    # print(summa)



    # filtered_data.append(sorted_data[0])
    # last_time = None
    # # current_time = sorted_data[0].recdt
    
    # for i in range(0,len(sorted_data)-1):
    #     if sorted_data[i+1].recdt - sorted_data[i].recdt >= delta[1] and (sorted_data[i+1].recdt- sorted_data[i].recdt) <= delta[2]:
    #         filtered_data.append(sorted_data[i+1])
            
    # for item in sorted_data:
    #     current_time = item.recdt

    #     # Если это первый элемент, добавляем его
    #     if last_time is None:
    #         filtered_data.append(item)
    #         last_time = current_time
    #         continue

    #     # Проверяем, соответствует ли текущий элемент интервалу
    #     if (current_time - last_time) >= delta[1] and (current_time - last_time) <= delta[2]:
    #         filtered_data.append(item)
    #         last_time = current_time

    # for item in sorted_data:
    #     current_time = item.recdt
    #     if last_time is None or (current_time - last_time) >= delta[1] and (current_time - last_time) <= delta[2]:
    #         filtered_data.append(item)
    #         last_time = current_time
    # print(*filtered_data,sep="\n")        

    # difference_array = []
    # for i in range(0,len(filtered_data)-1):
    #     if filtered_data[i].recdt - filtered_data[i+1].recdt <= delta[2]:
    #         dif_value = filtered_data[i+1].param_value-filtered_data[i].param_value
    #         dif_date_time = f"{filtered_data[i].recdt.strftime('%Y-%m-%d %H:%M')}-{filtered_data[i+1].recdt.strftime('%Y-%m-%d %H:%M')}"
    #         difference_array.append({'dif_date_time':dif_date_time, "dif_value":dif_value})
    #     else:
    #         expected_time = filtered_data[i].recdt + delta[1]
    #         dif_value = "Отсутствуют данные"
    #         dif_date_time = f"{filtered_data[i].recdt.strftime('%Y-%m-%d %H:%M')}-{expected_time.strftime('%Y-%m-%d %H:%M')}"
    #         difference_array.append({'dif_date_time':dif_date_time, "dif_value":dif_value})    

    # print(*difference_array,sep="\n")
    # # # Вывод результата
    # # for item in filtered_data:
    # #     print(f"Time: {item.recdt.strftime('%Y-%m-%d %H:%M')}, Value: {item.param_value} {item.unit}")
            
    # return difference_array 



class DevicesSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    recdt: int  # Unix-время (секунды с 1970-01-01)
    sid: str  # Идентификатор устройства
    param_name: str  # Название параметра
    ab_name: str  # Аббревиатура параметра
    param_value: float  # Значение параметра
    unit: str  # Единица измерения
    valid: str  # Статус валидности данных

# Пример данных с Unix-временем
data = [
    DevicesSchema(
        recdt=1696118400,  # 2023-10-01 00:00:00 UTC
        sid="555",
        param_name="Temperature",
        ab_name="T",
        param_value=25.5,
        unit="°C",
        valid="valid"
    ),
   
    DevicesSchema(
        recdt=1696125600,  # 2023-10-01 02:00:00 UTC
        sid="555",
        param_name="Temperature",
        ab_name="T",
        param_value=26.5,
        unit="°C",
        valid="valid"
    ),
     DevicesSchema(
        recdt=1696122000,  # 2023-10-01 01:00:00 UTC
        sid="555",
        param_name="Temperature",
        ab_name="T",
        param_value=26.0,
        unit="°C",
        valid="valid"
    ),
    DevicesSchema(
        recdt=1696129200,  # 2023-10-01 03:00:00 UTC
        sid="555",
        param_name="Temperature",
        ab_name="T",
        param_value=27.0,
        unit="°C",
        valid="valid"
    ),
    DevicesSchema(
        recdt=1696132800,  # 2023-10-01 04:00:00 UTC
        sid="555",
        param_name="Temperature",
        ab_name="T",
        param_value=27.5,
        unit="°C",
        valid="valid"
    ),
    DevicesSchema(
        recdt=1696136400,  # 2023-10-01 05:00:00 UTC
        sid="555",
        param_name="Temperature",
        ab_name="T",
        param_value=28.0,
        unit="°C",
        valid="valid"
    ),
    DevicesSchema(
        recdt=1696140000,  # 2023-10-01 06:00:00 UTC
        sid="555",
        param_name="Temperature",
        ab_name="T",
        param_value=28.5,
        unit="°C",
        valid="valid"
    ),
    DevicesSchema(
        recdt=1696143600,  # 2023-10-01 07:00:00 UTC
        sid="555",
        param_name="Temperature",
        ab_name="T",
        param_value=29.0,
        unit="°C",
        valid="valid"
    ),
    DevicesSchema(
        recdt=1696147200,  # 2023-10-01 08:00:00 UTC
        sid="555",
        param_name="Temperature",
        ab_name="T",
        param_value=29.5,
        unit="°C",
        valid="valid"
    ),
    DevicesSchema(
        recdt=1696150800,  # 2023-10-01 09:00:00 UTC
        sid="555",
        param_name="Temperature",
        ab_name="T",
        param_value=30.0,
        unit="°C",
        valid="valid"
    ),
]


grouped_data = grouped_data(data)
# Результат
for sid, devices in grouped_data.items():
    print(f"Device {sid}:")
    # for device in devices:
    #     print(f"  - {device.param_name}: {device.param_value} {device.unit} {device.recdt}")
out_data = []
for key,array in grouped_data.items():
    diff_data_device = difference_value_another(array,"2_hour")
    out_data.append({"sid":key,
                     "devices_values":diff_data_device})
# for item in out_data:
    # print(*item['devices_values'],sep="\n")

from pprint import pprint    
pprint(out_data)    


summ_array = []
for item in out_data:
    summ = summ_values(item['devices_values'])
    summ_array.append(summ)
print(summ_array)    




# time = 1696147200
# print(time)
# print(type(time))
# time_utc = datetime.fromtimestamp(time,tz=timezone.utc).replace(tzinfo=None)
# print(time_utc)
# print(type(time_utc))
# time_utc_str = time_utc.strftime('%Y-%m-%d %H:%M:%S')
# print(time_utc_str)
# print(type(time_utc_str))



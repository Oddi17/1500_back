from fastapi import APIRouter, Depends, HTTPException,status
from schemas.analitic_control import ACWaterSchema,ACRisingSchema
from typing import Annotated
from dependencies import analitic_control_service
from schemas.users import UsersSchema
from services.analitic_control import AnaliticControleService
from services.auth import role_dependency 

router = APIRouter(prefix="/analitic", tags=['Аналитический отчет'])

@router.post("/water")
async def sendwater(
    data: ACWaterSchema,
    analitic_control_service: Annotated[AnaliticControleService, Depends(analitic_control_service)],
    user: UsersSchema = Depends(role_dependency(["admin","operator"]))
):
    data.recdt = data.recdt.replace(tzinfo=None)
    data = data.model_dump()
    data['username'] = user.first_name
    res_id = await analitic_control_service.send_data(data)
    if not res_id:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Ошибка отправки данных")
    return {'message':'Данные успешно отправлены(исходная вода)'}

@router.post("/rising")
async def sendrising(
    data: ACRisingSchema,
    analitic_control_service: Annotated[AnaliticControleService, Depends(analitic_control_service)],
    user: UsersSchema = Depends(role_dependency(["admin","operator"]))
):
    data.recdt = data.recdt.replace(tzinfo=None)
    data = data.model_dump()
    data['username'] = user.first_name
    res_id = await analitic_control_service.send_data(data)
    if not res_id:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Ошибка отправки данных")
    return {'message':'Данные успешно отправлены(второй подъем)'}

@router.get("/journal")
async def getjournal(
    analitic_control_service: Annotated[AnaliticControleService, Depends(analitic_control_service)],
    start_time: str,
    end_time: str,
    user: UsersSchema = Depends(role_dependency(["admin","operator","user"])),
):
    data = await analitic_control_service.get_data(start_time,end_time) 
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="По запросу ничего не найдено")
    return data
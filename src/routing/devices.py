from typing import Annotated
from fastapi import APIRouter, Depends,HTTPException,status
from schemas.users import UsersSchema
from services.devices import DevicesService
from services.alarms import AlarmsService
from dependencies import devices_service, alarms_service
from fastapi.encoders import jsonable_encoder
from services.auth import role_dependency

router = APIRouter(prefix="/report", tags=['Оперативный отчет'])

@router.get("/waterbalance")
async def get_devices(
    devices_service: Annotated[DevicesService, Depends(devices_service)],
    start_time: str,
    end_time: str,
    sample : str | None = "1_hour",
    user: UsersSchema = Depends(role_dependency(["admin","user"]))
):  
    devices = await devices_service.get_devices(start_time,end_time,sample)
    if (not devices or len(devices["data_source"]) < 1):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="По запросу ничего не найдено")
    return jsonable_encoder(devices)

@router.get("/chemistry")
async def get_chemistry(
    devices_service: Annotated[DevicesService, Depends(devices_service)],
    start_time: str,
    end_time: str,
    sample: str | None = "1_hour",
    user: UsersSchema = Depends(role_dependency(["admin","user"]))
):
    data = await devices_service.get_chemistry(start_time,end_time,sample)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="По запросу ничего не найдено")
    return jsonable_encoder(data)


@router.get("/electricity")
async def get_chemistry(
    devices_service: Annotated[DevicesService, Depends(devices_service)],
    start_time: str,
    end_time: str,
    user: UsersSchema = Depends(role_dependency(["admin","user"]))
):
    data = await devices_service.get_electricity(start_time,end_time)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="По запросу ничего не найдено")
    return jsonable_encoder(data) 

@router.get("/reliability")
async def get_reliability(
    alarms_service: Annotated[AlarmsService, Depends(alarms_service)],
    start_time: str,
    end_time: str,
    user: UsersSchema = Depends(role_dependency(["admin","user"]))
):
    data = await alarms_service.get_reliability(start_time,end_time)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="По запросу ничего не найдено")
    return jsonable_encoder(data) 

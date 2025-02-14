from fastapi import Request,Depends
from repositories.devices import DevicesRepository
from repositories.users import UsersRepository
from repositories.alarms import AlarmsRepository
from repositories.analitic_control import AnaliticControl
from services.devices import DevicesService
from services.alarms import AlarmsService
from services.analitic_control import AnaliticControleService
# from services.auth import AuthService


def devices_service()->DevicesService:
    return DevicesService(DevicesRepository)

def alarms_service()->AlarmsService:
    return AlarmsService(AlarmsRepository)

def analitic_control_service()->AnaliticControleService:
    return AnaliticControleService(AnaliticControl)

# def users_service()->UsersService:
#     return UsersService(UsersRepository)

# def auth_service()->AuthService:
#     return AuthService(UsersRepository)




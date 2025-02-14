from models.devices import Devices
from utils.repository import SQLAlchemyRepository

class DevicesRepository(SQLAlchemyRepository):
    model = Devices
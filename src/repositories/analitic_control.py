from utils.repository import SQLAlchemyRepository
from models.analitic_control import AnaliticControl

class AnaliticControl(SQLAlchemyRepository):
    model = AnaliticControl
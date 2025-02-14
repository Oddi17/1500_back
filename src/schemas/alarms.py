from pydantic import BaseModel,ConfigDict

class AlarmsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id : int
    recdt: int
    sid: str
    alarmname: str
    abname: str
    status: bool

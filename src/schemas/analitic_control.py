from pydantic import BaseModel,ConfigDict
from datetime import datetime

class ACWaterSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    recdt: datetime
    location: str
    temperature: float
    ph: float
    color: float
    aluminum: float
    turbidity: float
    chlorides: float


class ACRisingSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    recdt: datetime
    location: str
    temperature: float
    ph: float
    color: float
    chlorine: float
    aluminum: float
    turbidity: float
    chlorides: float



class ACSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    recdt: datetime
    location: str
    temperature: float
    ph: float
    color: float
    chlorine: float | None
    aluminum: float
    turbidity: float
    chlorides: float
    username: str     
from typing import Optional
from pydantic import BaseModel,ConfigDict

class DevicesSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id : int
    recdt: int
    sid: str
    paramname: str
    abname: str
    paramvalue: float
    unit: str 
    valid: str

# class FiltersSchema(BaseModel):
#     sample: str
#     start_time: str
#     end_time: str
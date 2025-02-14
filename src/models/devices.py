from sqlalchemy.orm import Mapped,mapped_column
from database.db import Base
from sqlalchemy.types import String,REAL,CHAR,Integer
from schemas.devices import DevicesSchema


class Devices(Base):
    __tablename__ = "signalstab"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    recdt: Mapped[int] = mapped_column(Integer, nullable=True)  # recDt INTEGER
    sid: Mapped[str] = mapped_column(String(20), nullable=True)  # sid CHARACTER VARYING(20)
    paramname: Mapped[str] = mapped_column(String(50), nullable=True)  # ParamName CHARACTER VARYING(50)
    abname: Mapped[str] = mapped_column(String(8), nullable=True)  # AbName CHARACTER VARYING(8)
    paramvalue: Mapped[float] = mapped_column(REAL, nullable=True)  # ParamValue REAL
    unit: Mapped[str] = mapped_column(String(8), nullable=True)  # unit VARCHAR(8)
    valid: Mapped[str] = mapped_column(CHAR, nullable=True)  # valid CHAR

    def to_read_model(self) -> DevicesSchema:
        return DevicesSchema(
            id=self.id,
            recdt=self.recdt,
            sid=self.sid,
            paramname=self.paramname,
            abname=self.abname,
            paramvalue=self.paramvalue,
            unit=self.unit,
            valid=self.valid,
        )
    

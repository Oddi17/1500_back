from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy.types import String,Integer,Boolean
from database.db import Base
from schemas.alarms import AlarmsSchema



class Alarms(Base):
    __tablename__ = "alarmstab"

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    recdt: Mapped[int] = mapped_column(Integer, nullable=True)  # recDt INTEGER
    sid: Mapped[str] = mapped_column(String(20), nullable=True)  # sid CHARACTER VARYING(20)
    alarmname: Mapped[str] = mapped_column(String(50), nullable=True)  # ParamName CHARACTER VARYING(50)
    abname: Mapped[str] = mapped_column(String(8), nullable=True)  # AbName CHARACTER VARYING(8)
    status: Mapped[bool] = mapped_column(Boolean, nullable=True)

    def to_read_model(self)->AlarmsSchema:
        return AlarmsSchema(
            id=self.id,
            recdt=self.recdt,
            sid=self.sid,
            alarmname=self.alarmname,
            abname=self.abname,
            status=self.status
        )
from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped,mapped_column
from database.db import Base
from sqlalchemy.types import String,Integer,DateTime
from datetime import datetime
from schemas.analitic_control import ACSchema


class AnaliticControl(Base):
    __tablename__ = "analitic_control"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    recdt: Mapped[datetime] = mapped_column(DateTime, nullable=False) 
    location: Mapped[str] = mapped_column(String,nullable=False)
    temperature: Mapped[float] = mapped_column(Numeric(10,5),nullable=False)
    ph: Mapped[float] = mapped_column(Numeric(10,5),nullable=False)
    color: Mapped[float] = mapped_column(Numeric(10,5),nullable=False)
    chlorine: Mapped[float] = mapped_column(Numeric(10,5),nullable=True)
    aluminum: Mapped[float] = mapped_column(Numeric(10,5),nullable=False)
    turbidity: Mapped[float] = mapped_column(Numeric(10,5),nullable=False)
    chlorides: Mapped[float] = mapped_column(Numeric(10,5),nullable=False)
    username: Mapped[str] = mapped_column(String,nullable=False)

    def to_read_model(self) -> ACSchema:
        return ACSchema(
            id=self.id,
            recdt=self.recdt,
            location=self.location,
            temperature=self.temperature,
            ph=self.ph,
            color=self.color,
            chlorine=self.chlorine,
            aluminum=self.aluminum,
            turbidity=self.turbidity,
            chlorides=self.chlorides,
            username=self.username,
        )
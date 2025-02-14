from sqlalchemy.orm import Mapped,mapped_column
from database.db import Base
from sqlalchemy import String

from schemas.users import UsersSchema


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    login: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    
    role: Mapped[str] = mapped_column(server_default="is_user",nullable=False)

    # is_user: Mapped[bool] = mapped_column(default=True,server_default=text('true'),nullable=False)
    # is_admin: Mapped[bool] = mapped_column(default=True,server_default=text('false'),nullable=False)
    def to_read_model(self)->UsersSchema:
        return UsersSchema(
            id=self.id,
            first_name=self.first_name,
            login=self.login,
            password=self.password,
            role=self.role,
        )

        
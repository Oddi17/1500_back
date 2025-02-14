from pydantic import BaseModel,ConfigDict


class UsersSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str | None
    login: str
    password: str
    role: str


class UsersAuthSchema(BaseModel):
    login: str
    password: str
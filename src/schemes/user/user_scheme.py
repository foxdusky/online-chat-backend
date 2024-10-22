from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    id: int | None = Field(primary_key=True)
    fio: str | None
    username: str | None
    password: str | None
    salary: float | None
    bot_user_id: int | None = Field(foreign_key="bot_user.id")
    email: str | None
    phone: str | None


class User(UserBase, table=True):
    __tablename__ = "user"



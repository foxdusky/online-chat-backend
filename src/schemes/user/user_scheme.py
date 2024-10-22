from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship


class UserBase(SQLModel):
    id: int | None = Field(primary_key=True)
    username: str | None
    password: str | None
    reg_at: datetime | None = Field(default_factory=datetime.utcnow)


class User(UserBase, table=True):
    __tablename__ = "user"
    chats: list["Chat"] = Relationship(back_populates='users')
    messages: list["Message"] = Relationship(back_populates='')
    actions: list["MessageAction"] = Relationship(back_populates='user')


from schemes.chat.chat_scheme import Chat
from schemes.chat.message_scheme import Message
from schemes.chat.message_action_scheme import MessageAction

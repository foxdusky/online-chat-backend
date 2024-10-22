from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship


class UserBase(SQLModel):
    id: int | None = Field(primary_key=True)
    username: str = Field(nullable=False)
    password: str = Field(nullable=False)
    reg_at: datetime = Field(default_factory=datetime.utcnow)


class User(UserBase, table=True):
    __tablename__ = "user"
    chats: list["UsersInChat"] = Relationship(back_populates='user')  # many-to-many через UsersInChat
    messages: list["Message"] = Relationship(back_populates='user')
    actions: list["MessageAction"] = Relationship(back_populates='user')


class UserInfo(SQLModel):
    id: int
    username: str
    reg_at: datetime

    # TODO:
    last_online: datetime | None


from schemes.chat.users_in_chat_scheme import UsersInChat
from schemes.message.message_scheme import Message
from schemes.message.message_action_scheme import MessageAction

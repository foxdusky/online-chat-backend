from sqlmodel import SQLModel, Field, Relationship


class ChatBase(SQLModel):
    id: int | None = Field(primary_key=True)
    type: str = Field(default='private')
    user_count: int | None


class Chat(ChatBase, table=True):
    __tablename__ = "chat"
    users: list["User"] = Relationship(back_populates='chats')
    messages: list['Message'] = Relationship(back_populates='chat')


from schemes.user.user_scheme import User
from schemes.chat.message_scheme import Message

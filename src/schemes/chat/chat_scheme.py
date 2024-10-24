from sqlmodel import SQLModel, Field, Relationship

from schemes.chat.users_in_chat_scheme import UsersInChat


class ChatBase(SQLModel):
    id: int | None = Field(primary_key=True)
    type: str | None = Field(default='private')
    user_count: int | None


class Chat(ChatBase, table=True):
    __tablename__ = "chat"
    users: list["User"] = Relationship(back_populates='chats', link_model=UsersInChat)
    messages: list['Message'] = Relationship(back_populates='chat')


from schemes.chat.users_in_chat_scheme import UsersInChat
from schemes.message.message_scheme import Message

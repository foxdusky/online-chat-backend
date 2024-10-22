from sqlmodel import SQLModel, Field, Relationship


class ChatBase(SQLModel):
    id: int | None = Field(primary_key=True)
    type: str = Field(default='private')
    user_count: int | None


class Chat(ChatBase, table=True):
    __tablename__ = "chat"
    users: list["UsersInChat"] = Relationship(back_populates='chat')
    messages: list['Message'] = Relationship(back_populates='chat')


from schemes.chat.users_in_chat_scheme import UsersInChat
from schemes.chat.message_scheme import Message

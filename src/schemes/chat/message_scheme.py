from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship


class MessageBase(SQLModel):
    id: int | None = Field(primary_key=True)
    user_id: int = Field(foreign_key='user.id')
    chat_id: int = Field(foreign_key='chat.id')
    sent_at: datetime | None = Field(default_factory=datetime.utcnow)
    content: str


class Message(MessageBase, table=True):
    __tablename__ = "message"
    chat: "Chat" = Relationship(back_populates='messages')
    actions: list['MessageAction'] = Relationship(back_populates='message')
    user: "User" = Relationship(back_populates='messages')


from schemes.chat.chat_scheme import Chat
from schemes.chat.message_action_scheme import MessageAction
from schemes.user.user_scheme import User

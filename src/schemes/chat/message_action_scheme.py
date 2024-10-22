from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship


class MessageActionBase(SQLModel):
    id: int | None = Field(primary_key=True)
    message_id: int = Field(foreign_key="message.id")
    user_id: int = Field(foreign_key='user.id')
    done_at: datetime | None = Field(default_factory=datetime.utcnow)
    action: str


class MessageAction(MessageActionBase, table=True):
    __tablename__ = "message_action"
    message: "Message" = Relationship(back_populates='actions')
    user: 'User' = Relationship(back_populates='actions')


from schemes.chat.message_scheme import Message
from schemes.user.user_scheme import User

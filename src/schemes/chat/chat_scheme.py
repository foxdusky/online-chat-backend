from sqlmodel import SQLModel, Field, Relationship

from schemes.constant.request_scheme import DefaultRequestParam

from schemes.chat.users_in_chat_scheme import UsersInChat


class ChatBase(SQLModel):
    id: int | None = Field(primary_key=True)
    type: str | None = Field(default='private')
    user_count: int | None


class Chat(ChatBase, table=True):
    __tablename__ = "chat"
    users: list["User"] = Relationship(back_populates='chats', link_model=UsersInChat)
    messages: list['Message'] = Relationship(back_populates='chat')


class ChatWithUsers(ChatBase):
    users: list['UserInfo']


class ChatWithMessagesAndUsers(ChatBase):
    users: list['UserInfo']
    messages: list['Message']


class CreateChat(SQLModel):
    type: str | None
    users: list[int]


class RequestAll(DefaultRequestParam):
    chat_id: int


from schemes.user.user_scheme import User, UserInfo
from schemes.message.message_scheme import Message

ChatWithUsers.model_rebuild()
ChatWithMessagesAndUsers.model_rebuild()

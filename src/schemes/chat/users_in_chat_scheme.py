from sqlmodel import SQLModel, Field, Relationship


class UsersInChatBase(SQLModel):
    id: int | None = Field(primary_key=True)
    chat_id: int = Field(foreign_key='chat.id')
    user_id: int = Field(foreign_key='user.id')


class UsersInChat(UsersInChatBase, table=True):
    __tablename__ = "users_in_chat"
    user: "User" = Relationship(back_populates='chats')
    chat: "Chat" = Relationship(back_populates='users')


from schemes.user.user_scheme import User
from schemes.chat.chat_scheme import Chat

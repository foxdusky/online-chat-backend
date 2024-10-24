from sqlmodel import SQLModel, Field


class UsersInChatBase(SQLModel):
    id: int | None = Field(primary_key=True)
    chat_id: int = Field(foreign_key='chat.id')
    user_id: int = Field(foreign_key='user.id')


class UsersInChat(UsersInChatBase, table=True):
    __tablename__ = "users_in_chat"

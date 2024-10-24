from sqlalchemy import func
from sqlalchemy.orm import joinedload, selectinload
from sqlmodel import Session, select

from schemes.chat.chat_scheme import Chat, ChatWithMessagesAndUsers, ChatWithUsers
from schemes.chat.users_in_chat_scheme import UsersInChat


# Запрос на проверку существования private чата между пользователями
def check_private_chat_exists(session: Session, user_id: int, companion_id: int):
    st = (
        select(Chat)
        .join(UsersInChat)
        .where(
            Chat.type == 'private',
            UsersInChat.user_id.in_([user_id, companion_id])
        )
        .group_by(Chat.id)
        .having(
            func.count(UsersInChat.user_id) == 2
        )
    )

    return session.exec(st).first()


def get_all_chats(session: Session, user_id: int) -> list[ChatWithUsers]:
    st = (
        select(Chat)
        .join(UsersInChat)
        .where(UsersInChat.user_id == user_id)
        .options(selectinload(Chat.users))
    )
    result = session.exec(st).all()
    return list(result)


def get_chat_by_id(session: Session, chat_id: int) -> ChatWithMessagesAndUsers | None:
    st = select(Chat)
    st = st.where(Chat.id == chat_id)
    st = st.options(joinedload(Chat.messages), selectinload(Chat.users))
    return session.exec(st).first()


def create_chat(session: Session, chat: Chat):
    session.add(chat)
    session.commit()
    session.refresh(chat)
    return chat


def update_chat(session: Session, chat: Chat):
    db_chat = session.merge(chat)
    session.commit()
    session.refresh(db_chat)
    return db_chat


def delete_chat(session: Session, chat: Chat):
    session.delete(chat)
    session.commit()
    return chat

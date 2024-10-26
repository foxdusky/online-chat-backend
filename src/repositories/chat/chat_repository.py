from sqlalchemy import func, desc
from sqlalchemy.orm import joinedload, selectinload
from sqlmodel import Session, select

from schemes.chat.chat_scheme import Chat, ChatWithMessagesAndUsers, ChatWithUsers
from schemes.chat.users_in_chat_scheme import UsersInChat
from schemes.message.message_scheme import Message


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


def get_chat_by_id(
    session: Session,
    chat_id: int,
    limit: int | None = None,
    offset: int | None = None
) -> ChatWithMessagesAndUsers | None:
    # Запрос для получения чата с пользователями
    st = select(Chat).where(Chat.id == chat_id).options(selectinload(Chat.users))

    # Подзапрос для сообщений с лимитом и смещением
    messages_subquery = (
        select(Message)
        .where(Message.chat_id == chat_id)
        .order_by(desc(Message.id))
    )

    total_messages_count = session.exec(
        select(func.count(Message.id)).where(Message.chat_id == chat_id)
    ).first()

    if limit:
        messages_subquery = messages_subquery.limit(limit)
        pass

    if offset:
        messages_subquery = messages_subquery.offset(offset)

    messages_subquery = messages_subquery.subquery()

    st = st.options(joinedload(Chat.messages.and_(Message.id.in_(select(messages_subquery.c.id)))))

    chat = session.exec(st).first()

    return ChatWithMessagesAndUsers(
        **chat.model_dump(),
        users=chat.users,
        messages=chat.messages,
        count=total_messages_count
    )


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

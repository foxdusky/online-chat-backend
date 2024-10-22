from sqlmodel import Session, select

from schemes.chat.chat_scheme import Chat


def get_all_chats(session: Session) -> list[Chat]:
    st = select(Chat)
    result = session.exec(st).all()
    return list(result)


def get_chat_by_id(session: Session, chat_id: int) -> Chat | None:
    st = select(Chat)
    st = st.where(Chat.id == chat_id)
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

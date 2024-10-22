from sqlmodel import Session, select

from schemes.chat.users_in_chat_scheme import UsersInChat


def get_all_users_in_chat(session: Session) -> list[UsersInChat]:
    st = select(UsersInChat)
    result = session.exec(st).all()
    return list(result)


def get_users_in_chat_by_id(session: Session, users_in_chat_id: int) -> UsersInChat | None:
    st = select(UsersInChat)
    st = st.where(UsersInChat.id == users_in_chat_id)
    return session.exec(st).first()


def create_users_in_chat(session: Session, users_in_chat: UsersInChat):
    session.add(users_in_chat)
    session.commit()
    session.refresh(users_in_chat)
    return users_in_chat


def update_users_in_chat(session: Session, users_in_chat: UsersInChat):
    db_users_in_chat = session.merge(users_in_chat)
    session.commit()
    session.refresh(db_users_in_chat)
    return db_users_in_chat


def delete_users_in_chat(session: Session, users_in_chat: UsersInChat):
    session.delete(users_in_chat)
    session.commit()
    return users_in_chat

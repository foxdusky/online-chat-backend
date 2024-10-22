from sqlmodel import Session, select

from schemes.message.message_scheme import Message


def get_all_messages(session: Session) -> list[Message]:
    st = select(Message)
    result = session.exec(st).all()
    return list(result)


def get_message_by_id(session: Session, message_id: int) -> Message | None:
    st = select(Message)
    st = st.where(Message.id == message_id)
    return session.exec(st).first()


def create_message(session: Session, message: Message):
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


def update_message(session: Session, message: Message):
    db_message = session.merge(message)
    session.commit()
    session.refresh(db_message)
    return db_message


def delete_message(session: Session, message: Message):
    session.delete(message)
    session.commit()
    return message

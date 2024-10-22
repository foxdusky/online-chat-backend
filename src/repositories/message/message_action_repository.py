from sqlmodel import Session, select

from schemes.message.message_action_scheme import MessageAction


def get_all_message_actions(session: Session) -> list[MessageAction]:
    st = select(MessageAction)
    result = session.exec(st).all()
    return list(result)


def get_message_action_by_id(session: Session, message_action_id: int) -> MessageAction | None:
    st = select(MessageAction)
    st = st.where(MessageAction.id == message_action_id)
    return session.exec(st).first()


def create_message_action(session: Session, message_action: MessageAction):
    session.add(message_action)
    session.commit()
    session.refresh(message_action)
    return message_action


def update_message_action(session: Session, message_action: MessageAction):
    db_message_action = session.merge(message_action)
    session.commit()
    session.refresh(db_message_action)
    return db_message_action


def delete_message_action(session: Session, message_action: MessageAction):
    session.delete(message_action)
    session.commit()
    return message_action

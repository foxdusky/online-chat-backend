from fastapi import HTTPException, status
from sqlmodel import Session

from models.access.access_model import check_user_in_chat
from repositories.message import message_repository
from schemes.message.message_scheme import Message, MessageSend
from schemes.user.user_scheme import User


def get_message_by_id(session: Session, message_id: int) -> Message:
    message = message_repository.get_message_by_id(session, message_id)

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Message with ID {message_id} not found",
        )
    return message


def send_message(session: Session, body: MessageSend, current_user: User) -> None:
    check_user_in_chat(session=session, chat_id=body.chat_id, user_id=current_user.id)
    message = Message(
        user_id=current_user.id,
        **body.model_dump()
    )
    message_repository.create_message(session, message)
    return status.HTTP_200_OK

def delete_message(session: Session, message_id: int):
    db_message = get_message_by_id(session, message_id)
    return message_repository.delete_message(session, db_message)


def update_message(session: Session, message: Message) -> Message:
    return message_repository.update_message(session, message)

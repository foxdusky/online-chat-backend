from fastapi import HTTPException, status
from sqlmodel import Session

from repositories.chat import users_in_chat_repository
from repositories.chat.chat_repository import check_private_chat_exists


def check_user_in_chat(session: Session, user_id: int, chat_id: int):
    access = users_in_chat_repository.check_user_in_chat(session=session, user_id=user_id, chat_id=chat_id)
    if not access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You don't have access to this chat",
        )


def check_create_chat(session: Session, user_id: int, companion_id: int):
    check = check_private_chat_exists(session, user_id, companion_id)
    print(check)
    if check:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You already have chat with that user",
        )

from fastapi import HTTPException, status
from sqlmodel import Session

from constant.chat_type import ChatType
from models.access.access_model import check_user_in_chat, check_create_chat
from repositories.chat import chat_repository, users_in_chat_repository
from schemes.chat.chat_scheme import Chat, RequestAll, CreateChat, ChatWithUsers, ChatWithMessagesAndUsers
from schemes.chat.users_in_chat_scheme import UsersInChat
from schemes.user.user_scheme import User


def get_chat_by_id(session: Session, body: RequestAll, current_user: User) -> Chat:
    chat = chat_repository.get_chat_by_id(session, body.chat_id)
    check_user_in_chat(session, user_id=current_user.id, chat_id=body.chat_id)

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat with ID {body.chat_id} not found",
        )
    return chat


def get_all_chats(session: Session, current_user: User) -> list[ChatWithUsers]:
    return chat_repository.get_all_chats(session, current_user.id)


def create_chat(session: Session, body: CreateChat, current_user: User) -> ChatWithMessagesAndUsers:
    # Check for private chat
    if body.type == ChatType.PRIVATE:
        # Check for len of users to create in chat
        if len(body.users) > 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Too many users for private chat",
            )
        # Check for existing private chat between these users
        check_create_chat(session, user_id=current_user.id, companion_id=body.users[0])
        if body.users[0] == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"U can't create chat with u own",
            )
    elif body.type == ChatType.GROUP:
        pass

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Wrong chat type",
        )

    body.users.append(current_user.id)

    # Creating chat in database
    chat = Chat(
        type=body.type,
        user_count=len(body.users)
    )
    chat = chat_repository.create_chat(session, chat)

    # Creating user to chat relationship records in db
    for user_id in body.users:
        user_in_chat = UsersInChat(
            chat_id=chat.id,
            user_id=user_id
        )
        users_in_chat_repository.create_users_in_chat(session, user_in_chat)

    return chat_repository.get_chat_by_id(session, chat.id)


# TODO add recursive deletion
def delete_chat(session: Session, chat_id: int):
    # check_user_in_chat(session, user_id=current_user.id, chat_id=body.chat_id)

    db_chat = get_chat_by_id(session, chat_id)
    return chat_repository.delete_chat(session, db_chat)


# Not in need nowadays
def update_chat(session: Session, chat: Chat) -> Chat:
    # check_user_in_chat(session, user_id=current_user.id, chat_id=body.chat_id)

    return chat_repository.update_chat(session, chat)

from fastapi import APIRouter, Depends
from sqlmodel import Session

from constant.ws_queues import WSQueue
from db import get_session
from middleware.ws_queue_decorator import ws_queue
from models.chat import chat_model
from models.user.auth_model import get_current_user
from schemes.chat.chat_scheme import Chat, RequestAll, ChatWithMessagesAndUsers, CreateChat, ChatWithUsers
from schemes.user.user_scheme import User

queue_name = WSQueue.CHAT

chat_router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@chat_router.get("/", response_model=list[ChatWithUsers])
async def get_all_chats(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return chat_model.get_all_chats(session, current_user)


@chat_router.post("/id/", response_model=ChatWithMessagesAndUsers)
async def get_by_id(
    body: RequestAll,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return chat_model.get_chat_by_id(session, body, current_user)


@chat_router.post("/", response_model=Chat)
@ws_queue(queue_name)
async def create_chat(
    body: CreateChat,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return chat_model.create_chat(session, body, current_user)

# Would be in need later P.S. Hasn't logix

# @chat_router.put("/", response_model=Chat)
# @ws_queue(queue_name)
# async def update_chat(
#     chat: Chat,
#     session: Session = Depends(get_session),
#     current_user: User = Depends(get_current_user),
# ):
#     return chat_model.update_chat(session, chat)

# Would be in need later P.S. Hasn't logix

# @chat_router.delete("/{chat_id}", response_model=Chat)
# @ws_queue(queue_name)
# async def delete_chat(
#     chat_id: int,
#     session: Session = Depends(get_session),
#     current_user: User = Depends(get_current_user),
# ):
#     return chat_model.delete_chat(session, chat_id)

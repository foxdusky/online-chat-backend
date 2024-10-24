from fastapi import APIRouter, Depends
from sqlmodel import Session

from constant.ws_queues import WSQueue
from db import get_session
from middleware.ws_queue_decorator import ws_queue
from models.message import message_model
from models.user.auth_model import get_current_user
from schemes.message.message_scheme import Message, MessageSend
from schemes.user.user_scheme import User

queue_name = WSQueue.MESSAGE

message_router = APIRouter(
    prefix="/message",
    tags=["message"]
)


@message_router.post("/", response_model="")
@ws_queue(queue_name)
async def send_message(
    body: MessageSend,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return message_model.send_message(session, body, current_user)

# Would be in need later P.S. Hasn't logix

# @message_router.put("/", response_model=message)
# @ws_queue(queue_name)
# async def update_message(
#     message: message,
#     session: Session = Depends(get_session),
#     current_user: User = Depends(get_current_user),
# ):
#     return message_model.update_message(session, message)

# Would be in need later P.S. Hasn't logix

# @message_router.delete("/{message_id}", response_model=message)
# @ws_queue(queue_name)
# async def delete_message(
#     message_id: int,
#     session: Session = Depends(get_session),
#     current_user: User = Depends(get_current_user),
# ):
#     return message_model.delete_message(session, message_id)

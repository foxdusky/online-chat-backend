from fastapi import APIRouter, Depends
from sqlmodel import Session

from constant.ws_queues import WSQueue
from db import get_session
from middleware.ws_queue_decorator import ws_queue
from models.user import user_model
from models.user.auth_model import get_current_user
from schemes.user.user_scheme import User

queue_name = WSQueue.USER

user_router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@user_router.get("/", response_model=list[User])
async def get_all_users(
        session: Session = Depends(get_session),
        current_user: User = Depends(get_current_user),
):
    return user_model.get_all_users(session)


@user_router.get("/{user_id}", response_model=User)
async def get_by_id(
        user_id: int,
        session: Session = Depends(get_session),
        current_user: User = Depends(get_current_user),
):
    return user_model.get_user_by_id(session, user_id)


@user_router.get("/login/{login}", response_model=User)
async def get_by_login(
        login: str,
        session: Session = Depends(get_session),
        current_user: User = Depends(get_current_user),
):
    return user_model.get_by_login(session, login)


@user_router.post("/", response_model=User)
@ws_queue(queue_name)
async def create_user(
        user: User,
        session: Session = Depends(get_session),
        current_user: User = Depends(get_current_user),
):
    return user_model.create_user(session, user, current_user)


@user_router.put("/", response_model=CurrentUser)
@ws_queue(queue_name)
async def update_user(
        user: UserEdit,
        session: Session = Depends(get_session),
        current_user: User = Depends(get_current_user),
):
    return user_model.update_user(session, user, current_user)


@user_router.delete("/{user_id}", response_model=User)
@ws_queue(queue_name)
async def delete_user(
        user_id: int,
        session: Session = Depends(get_session),
        current_user: User = Depends(get_current_user),
):
    return user_model.delete_user(session, user_id, current_user)

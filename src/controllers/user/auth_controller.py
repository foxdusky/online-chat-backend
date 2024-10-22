from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from db import get_session
from models.user import auth_model
from models.user.auth_model import get_current_user
from schemes.user.user_scheme import User
from schemes.user.auth_scheme import AuthToken

auth_router = APIRouter(
    prefix='/auth',
    tags=["Auth"]
)


@auth_router.post("/sign_in/", response_model=AuthToken)
async def sign_in(
        session: Session = Depends(get_session),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    token = auth_model.sign_in(session, form_data.username, form_data.password)
    return token


@auth_router.get(
    "/generate_token/",
    response_model=AuthToken,
    description="Returns JWT token by user database id and expiry in minutes")
async def generate_token(
        user_id: int,
        expiry: int | None,
        current_user: User = Depends(get_current_user)
):
    return auth_model._get_auth_token(user_id, expiry)

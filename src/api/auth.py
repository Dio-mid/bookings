from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import UserAlreadyExistsException, UserEmailAlreadyExistsHTTPException, EmailNotRegisteredException, \
    EmailNotRegisteredHTTPException, IncorrectPasswordException, IncorrectPasswordHTTPException
from src.schemes.users import UserApiAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


# Cookie - хранилище данных, которые автоматически отправляются с каждым запросом на бекэнд, JWT должен быть в cookie


@router.post("/register")
async def register_user(data: UserApiAdd, db: DBDep):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException
    return {"status": "OK"}


@router.post("/login")
async def login_user(data: UserApiAdd, response: Response, db: DBDep):
    try:
        access_token = await AuthService(db).login_user(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", access_token)  # Добавляет JWT в cookie
    return {"access_token": access_token}


@router.get("/auth_user")
async def auth_user(user_id: UserIdDep, db: DBDep):
    return await AuthService(db).get_one_or_none_user(user_id)


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}

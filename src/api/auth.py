from fastapi import APIRouter, HTTPException, Response, Request

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemes.users import UserApiAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


#Cookie - хранилище данных, которые автоматически отправляются с каждым запросом на бекэнд, JWT должен быть в cookie


@router.post("/register")
async def register_user(user_data: UserApiAdd):
    hashed_password = AuthService().hash_password(user_data.password)
    new_user_data = UserAdd(email=user_data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()
    return {"status": "OK"}

@router.post("/login")
async def login_user(
        data: UserApiAdd,
        response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token) # Добавляет JWT в cookie
        return {"access_token": access_token}

@router.get("/only_auth")
async def only_auth(request: Request):
    access_token = request.cookies
    if access_token is None:
        return None
    return access_token

from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.schemes.users import UserApiAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


#Cookie - хранилище данных, которые автоматически отправляются с каждым запросом на бекэнд, JWT должен быть в cookie


@router.post("/register")
async def register_user(user_data: UserApiAdd, db: DBDep):
    hashed_password = AuthService().hash_password(user_data.password)
    new_user_data = UserAdd(email=user_data.email, hashed_password=hashed_password)
    await db.users.add(new_user_data)
    await db.commit()
    return {"status": "OK"}

@router.post("/login")
async def login_user(data: UserApiAdd, response: Response, db: DBDep):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Пароль неверный")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token) # Добавляет JWT в cookie
    return {"access_token": access_token}

@router.get("/auth_user")
async def auth_user(user_id: UserIdDep,  db: DBDep):
    user = await db.users.get_one_or_none(id=user_id)
    return user

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}

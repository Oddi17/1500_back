from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response,status
from schemas.users import UsersAuthSchema, UsersSchema,UsersCreateSchema,UsersChange,UsersPassword
from services.auth import authenticate_user, role_dependency,verify_password,get_user_role,create_access_token,get_current_user,get_password_hash
from services.users import UsersService
from dependencies import users_service


  
router = APIRouter(prefix='/auth', tags=['Авторизация'])

@router.get("/",summary="Проверка авторазиции")
async def get_auth(user: UsersSchema = Depends(get_current_user)):
    role = get_user_role(user.role)
    return {'role':role,'username':user.first_name,'login':user.login}


@router.post("/login",summary="Авторизация пользователя")
async def authorization_user(
            response: Response, 
            credentials: UsersAuthSchema,
            ):
    user = await authenticate_user(login=credentials.login,password=credentials.password)
    check_cred = verify_password(credentials.password,user.password)
    if not check_cred:
        raise HTTPException(status_code=401,detail="Неверные учетные данные")
    role = get_user_role(user.role)
    access_token = create_access_token({"sub": str(user.id),"role":str(role)})
    response.set_cookie(
                    key="user_access_token", 
                    value=access_token,
                    # secure=True,
                    # samesite="None",
                    httponly=True,
                    max_age=18000,   # Кука будет жить 5 час
                    #expires=expires, 
                    path="/"        # Доступна для всех путей
                )
    return {'role':role,'username':user.first_name,'login':user.login}

@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(key="user_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}

@router.get("/show/user",summary="Показать всех пользователей")
async def show_users(
                        users_service: Annotated[UsersService, Depends(users_service)],
                        user: UsersSchema = Depends(role_dependency(["admin"]))
                     ):
    users = await users_service.get_all_users()
    if not users:
        raise HTTPException(status_code=404,detail="Список пользователей пуст")
    return users

@router.post("/create/user",summary="Создание пользователя")
async def create_user(
                        users_service: Annotated[UsersService, Depends(users_service)], 
                        credentials : UsersCreateSchema,
                        user: UsersSchema = Depends(role_dependency(["admin"]))
                    ):
    res_id = await users_service.create_user(credentials)
    if not res_id:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Ошибка создания пользователя")
    return {'message':'Пользователь успешно создан'}

@router.delete("/delete/user/{user_id}",summary="Удаление пользователя")
async def delete_user(
                        users_service: Annotated[UsersService, Depends(users_service)],
                        user_id : int,
                        user: UsersSchema = Depends(role_dependency(["admin"]))
                    ):
    res = await users_service.delete_user(user_id)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Такого пользователя не существует")
    return {'message':'Пользователь успешно удален'}

@router.put("/change/user/role")
async def change_role_user(
                            users_service: Annotated[UsersService, Depends(users_service)],
                            change_user_data: UsersChange,
                            user: UsersSchema = Depends(role_dependency(["admin"]))
                        ):
    res = await users_service.change_role_user(change_user_data)
    if not res:
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Ошибка изменения роли пользователя")
    return {'message':'Роль пользователя успешно изменена'}

@router.put("/change/user/password")
async def change_user_password(
                        users_service: Annotated[UsersService, Depends(users_service)],
                        change_user_data: UsersPassword,
                        user: UsersSchema = Depends(role_dependency(["admin"]))
                    ):
    res = await users_service.change_password_user(change_user_data)
    if not res:
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Ошибка изменения пароля пользователя")
    return {'message':'Пароль пользователя успешно изменен'}
from fastapi import APIRouter, Depends, HTTPException, Response
from schemas.users import UsersAuthSchema, UsersSchema
from services.auth import authenticate_user,verify_password,get_user_role,create_access_token,get_current_user

  
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

    
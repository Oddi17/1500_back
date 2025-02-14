from fastapi import Request, HTTPException, status, Depends
from schemas.users import UsersSchema
from jose import jwt, JWTError
from passlib.context import CryptContext
from config import settings
from datetime import datetime, timezone, timedelta
from repositories.users import UsersRepository


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_role(user_role)->str:
        role_map= {
            "is_user" : "user",
            "is_admin" : "admin",
            "is_operator" : "operator",
        }
        return role_map.get(user_role,"")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire}) #время истечения токена
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encode_jwt

def get_token(request: Request):
    token = request.cookies.get('user_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Пользователь не авторизован')
    return token

async def authenticate_user(login,password):
    user = await UsersRepository.get_user_by_login(login)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Пользователь не найден")
    user = user.to_read_model()
    check_cred = verify_password(password,user.password)
    if not check_cred:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Неверные учетные данные")
    return user
    

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get('sub')
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Ошибка авторизации(id)')
        user = await UsersRepository.get_user_by_id(int(user_id))
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Пользователь не найден')
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Ошибка авторизации')
    return user.to_read_model()

def role_dependency(required_roles: list):
    """Фабрика зависимостей для проверки ролей"""
    def dependency(user: dict = Depends(get_current_user)):
        role = get_user_role(user.role)
        user.role = role
        if role not in required_roles:
            raise HTTPException(status_code=403, detail="Доступ запрещен")
        return user
    return dependency

# def req_role_admin(user: UsersSchema = Depends(get_current_user)): 
#     allowed_roles=['admin']
#     role = get_user_role(user.role)
#     if role not in allowed_roles:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Нет доступа"
#         )
#     return user

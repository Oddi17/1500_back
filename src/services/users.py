from utils.repository import AbstractRepository
from services.auth import get_password_hash,get_user_role
class UsersService:
    def __init__(self,users_repo:type[AbstractRepository]):
        self.users_repo = users_repo()
    
    async def get_all_users(self):
        users = await self.users_repo.get_all_users()
        #Убрать самого админа
        # Убираем поле password при сериализации
        serialized_users = [user.model_dump(exclude={"password"}) for user in users if user.id != 1]
        for user in serialized_users:
            user['role'] = get_user_role(user['role'],1)
        return serialized_users
    
    async def create_user(self,user_data):
        hash_password_user = get_password_hash(user_data.password)
        role_user = get_user_role(user_data.role,1)
        user_data.password = hash_password_user
        user_data.role = role_user
        user_data = user_data.model_dump()
        user_id = await self.users_repo.add(user_data)
        return user_id
    
    async def delete_user(self,user_id):
        res = await self.users_repo.delete(self.users_repo.model.id == user_id)
        return res
    
    async def change_role_user(self,user_data):
        user_role = get_user_role(user_data.role,1)
        user_id = user_data.id
        user_data = {"role":user_role}
        res = await self.users_repo.change(user_id,user_data)
        return res
    
    async def change_password_user(self,user_data):
        hash_password_user = get_password_hash(user_data.password)
        user_password = hash_password_user
        user_id = user_data.id
        user_data = {"password":user_password}
        res = await self.users_repo.change(user_id,user_data)
        return res
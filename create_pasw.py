from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

try:
    while True:
        last_name = input("Введи фамилию:")
        password_str = input("Введи пароль:")
        hash_pas = get_password_hash(password_str)
        print(hash_pas)
        with open("create.txt","+a") as file:
            file.write(f"{last_name}:{hash_pas}\n")
except KeyboardInterrupt as e:
    pass     



import bcrypt
import random

from datetime import date
from database import User

from fastapi import HTTPException

from peewee import OperationalError

from Passwords.password import hashed_password

###############################################################################

def create_username (name: str, last_name:str):

    username_base = (name[:2] + last_name[:2].lower())
    id_random = random.randint(0,9) * 10 + random.randint(0,9)

    username = f'{username_base}{id_random}'

    while User.select().where(User.username == username).exists():

        id_random = random.randint(0,9) * 10 + random.randint(0,9)
        username = f'{username_base}{id_random}'
    
    return username

async def validate_user(username: str, password: str):

    if User.select().where(User.email == username).exists():
        raise HTTPException(status_code=400, detail="El usuario no existe")
    
    usuario = User.get(User.username == username)
    salt = usuario.salt

    hashed_password_usuario = bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8'))
    hashed_password_usuario = (hashed_password_usuario[:10])


    # Compara el hash generado con el hash almacenado en la tabla
    if hashed_password_usuario == usuario.password.encode('utf-8'):
        return True  # La contraseña es válida
    else:
        return False  # La contraseña no es válida

async def get_user(username):

    user = User.get_or_none(User.username == username)
    print(username)

    if user:
        return user.__dict__["__data__"]
    else:
        raise HTTPException(status_code=404, detail=f"Usuario '{username}' no encontrado")

async def get_all_users():
    users = list(User.select())

    return [{"id": user.id, "name": user.name, "email": user.email} for user in users]

async def create_user(user_request):

    if User.select().where(User.email == user_request.email).exists():
        raise HTTPException(status_code=400, detail="El correo electrónico ya está en uso")

    username = create_username(user_request.name, user_request.last_name)

    password_hashed, salt = hashed_password(user_request.password)

    try:
        user = User.create(
            username=username,
            name=user_request.name,
            last_name=user_request.last_name,
            password=user_request.password,
            rol=user_request.rol,  # Asegúrate de usar roles válidos aquí
            email=user_request.email,
            salt=salt,
            fecha_registro=date.today().strftime("%d/%m/%Y")
        )

        
    except OperationalError as e:
        if "Check constraint 'users_chk_1' is violated" in str(e):
            raise HTTPException(status_code=400, detail="El valor proporcionado para 'rol' no es válido. Use 'admin' o 'user'.")
        else:
            raise HTTPException(status_code=500, detail="Error interno del servidor. Por favor, contacta al administrador.")

    return {"mensaje": "Usurio creado con exito"}

async def update_user(user_request, username):

    user = User.get_or_none(User.username == username)

    if user:
        # Actualiza los campos del usuario con los valores proporcionados
        user.name = user_request.name
        user.rol = user_request.rol
        user.email = user_request.email
        user.save()
        return {"mensaje": "Datos del usuario actualizados exitosamente"}
    else:
        raise HTTPException(status_code=404, detail=f"Usuario: '{username}' no encontrado")

async def delete_user(username, password):

    user = User.select().where((User.username == username) & (User.password == password)).first()

    if user:
        user.delete_instance()
        return {"mensaje": f"Usuario '{username}' eliminado exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="El usuario no existe")


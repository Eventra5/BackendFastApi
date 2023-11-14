import bcrypt
import random

from Passwords.password import hashed_password

from database import User

from schemas import UsuarioCreate, UsuarioBase

from fastapi import HTTPException

from datetime import date

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

def create_username (name: str, last_name:str):

    username_base = (name[:2] + last_name[:2].lower())
    id_random = random.randint(0,9) * 10 + random.randint(0,9)

    username = f'{username_base}{id_random}'

    while User.select().where(User.username == username).exists():

        id_random = random.randint(0,9) * 10 + random.randint(0,9)
        username = f'{username_base}{id_random}'
    
    return username

async def get_user(user_get: str):

    user = User.get_or_none(User.name == user_get)

    if user:
        return user.__dict__["__data__"]
    else:
        raise HTTPException(status_code=404, detail=f"Usuario '{user_get}' no encontrado")

async def get_all_users():
    users = list(User.select())

    return [{"id": user.id, "name": user.name, "email": user.email} for user in users]

async def create_user(user_request: UsuarioCreate):

    fecha_actual = date.today()
    fecha_iniciof = fecha_actual.strftime("%d/%m/%Y")


    if User.select().where(User.email == user_request.email).exists():
        raise HTTPException(status_code=400, detail="El correo electrónico ya está en uso")

    username = create_username(user_request.name, user_request.last_name)

    password_hashed, salt = hashed_password(user_request.password)

    user = User.create(
        username = username,
        name = user_request.name,
        last_name = user_request.last_name,
        password = user_request.password,
        rol = user_request.rol,
        email = user_request.email,
        salt = salt,
        fecha_registro = fecha_iniciof
    )

    return 'Usuario creado con exito'

async def update_user(user_update: str, usuario_update: UsuarioBase):
    user = User.get_or_none(User.name == user_update)

    if user:
        # Actualiza los campos del usuario con los valores proporcionados
        user.name = usuario_update.name
        user.rol = usuario_update.rol
        user.email = usuario_update.email
        user.save()
        return {"mensaje": f"Datos del usuario '{usuario_update}' actualizados exitosamente"}
    else:
        raise HTTPException(status_code=404, detail=f"Usuario '{user_update}' no encontrado")

async def delete_user(user_delete, password_delete):

    user = User.select().where((User.name == user_delete) & (User.password == password_delete)).first()

    if user:
        user.delete_instance()
        return {"mensaje": f"Usuario '{user_delete}' eliminado exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="El usuario no existe")


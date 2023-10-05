from database import User

from schemas import UsuarioCreate, UsuarioBase

from fastapi import HTTPException


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

    if User.select().where(User.email == user_request.email).exists():
        raise HTTPException(status_code=400, detail="El correo electrónico ya está en uso")

    user = User.create(
        name = user_request.name,
        password = user_request.password,
        rol = user_request.rol,
        email = user_request.email
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

    user = User.select().where(User.name == user_delete && User.password == password_delete ).first()

    if user:
        user.delete_instance()
        return {"mensaje": f"Usuario '{user_delete}' eliminado exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="El usuario no existe")


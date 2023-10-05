from typing import Optional
from pydantic import BaseModel, EmailStr

class UsuarioBase(BaseModel):
    name: str
    rol: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    password: str
    fecha_registro: str

class Usuario(UsuarioBase):
    id: int

class updatepass(BaseModel):
    password: str






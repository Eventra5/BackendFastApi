from fastapi import FastAPI
from fastapi import HTTPException
from datetime import datetime

from database import User, Company
from database import DB as connection 
from database import create_database

from schemas import CompanyResponse, UsuarioBase, UsuarioCreate, CompanyCreate

import Pages.users as user_page
import Pages.companys as company_page

app = FastAPI(title="Estacionamiento", description="Software para el uso y administracion de estacionamientos", version='1.0.1')

create_database('estacionamiento')

#Eventos para el servidor
#region event server
@app.on_event('startup')
def startup():
        
    if connection.is_closed():
        connection.connect()

    connection.create_tables([User])
    connection.create_tables([Company])
    
@app.on_event('shutdown')
def shutdown():

    if not connection.is_closed():
            connection.close()  

#endregion

#Peticiones para los usuarios
#region users
@app.get("/users/{user_get}")
async def get_user(user_get: str):
    return await user_page.get_user(user_get)

@app.get("/users")
async def get_all_users():
    return await user_page.get_all_users()

@app.post('/users')
async def create_user(user_request: UsuarioCreate):
    return await user_page.create_user(user_request)

@app.put("/users/{user_update}")
async def update_user(user_update: str, usuario_update: UsuarioBase):
    return await user_page.update_user(user_update, usuario_update)

@app.delete('/users/{user_delete}/{password_delete}')
async def delete_user(user_delete,password_delete):
    return await user_page.delete_user(user_delete,password_delete)
#endregion

@app.post("/company/", response_model=CompanyResponse)
async def create_company(company_request: CompanyCreate):
    return await company_page.create_company(company_request)

                
#env\scripts\activate.bat
#uvicorn main:app --reload
#pip install peewee
#pip install mysql
#pip install sqlalchemy

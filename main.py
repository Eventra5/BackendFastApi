from fastapi import FastAPI
from fastapi import HTTPException
from datetime import datetime

from database import DB as connection 
from database import User, Company, Discount
from database import create_database

from schemas import CompanyResponse, UsuarioBase, UsuarioCreate, CompanyCreate, DiscountBase, DiscountCreate

import Pages.users as user_page
import Pages.companys as company_page
import Pages.discounts as discounts_page

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
    connection.create_tables([Discount])

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

#Peticiones para las empresas
#region companies
@app.get("/company/{company_get}")
async def get_company(company_get: str):
    return await company_page.get_company(company_get)

@app.get("/company")
async def get_all_companies():
    return await company_page.get_all_companies()

@app.post("/company/", response_model=CompanyResponse)
async def create_company(company_request: CompanyCreate):
    return await company_page.create_company(company_request)

@app.delete('/company/{company_name}')
async def delete_company(company_name):
    return await company_page.delete_company(company_name)
#endregion
                
#Peticiones para los descuentos
#region discounts

@app.get("/discount/{discount_id}")
async def get_discount(discount_id: str):
    return await discounts_page.get_discount(discount_id)

@app.get("/discount/{company}")
async def get_discounts_by_company_name(company_get: str):
    return await discounts_page.get_discounts_by_company_name(company_get)

@app.post("/discount/", response_model=DiscountBase)
async def create_discount(discount: DiscountCreate, company_id: int):
    return await discounts_page.create_discount(discount, company_id)

@app.delete('/discount/{discount_id}')
async def delete_discount(discount_id):
    return await discounts_page.delete_discount(discount_id)
#endregion

#Peticiones para los clientes
#region client


#endregion

#env\scripts\activate.bat
#uvicorn main:app --reload
#pip install peewee
#pip install mysql
#pip install sqlalchemy

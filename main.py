from typing import Optional
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from database import DB as connection 
from database import User, Company, Discount, Customer, Customer_discount, AperturaCaja, CierreCaja, Transacciones, Planes_cobro
from database import create_database

from schemas import CompanyResponse, UsuarioCreate, CompanyCreate, DiscountCreate, CustomerCreate, TransaccionCreate, PlanesCreate
from schemas import UsuarioBase, DiscountBase, AbrirCajaBase

from peewee import DoesNotExist

import Pages.users as user_page
import Pages.companys as company_page
import Pages.discounts as discounts_page
import Pages.customers as customer_page
import Pages.login as login_page
import Pages.caja as caja_page
import Pages.planes_cobro as plan_page
import Pages.transaciones as transacciones_page

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Estacionamiento", description="Software para el uso y administracion de estacionamientos", version='1.0.1')

create_database('estacionamiento')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#Eventos para el servidor
#region event server
@app.on_event('startup')
def startup():
        
    if connection.is_closed():
        connection.connect()

    connection.create_tables([User])
    connection.create_tables([Company])
    connection.create_tables([Discount])
    connection.create_tables([Customer])
    connection.create_tables([Customer_discount])
    connection.create_tables([AperturaCaja])
    connection.create_tables([CierreCaja])
    connection.create_tables([Transacciones])
    connection.create_tables([Planes_cobro])

@app.on_event('shutdown')
def shutdown():

    if not connection.is_closed():
            connection.close()  

#endregion

#Peticiones para el login
#region login

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.post('/login', tags=["Login"])
async def login(request_login: OAuth2PasswordRequestForm = Depends()):
    return await login_page.login_user(request_login)
    
#endregion


#Peticiones para los usuarios
#region users

@app.get("/users/{username}", tags=["User"])
async def get_user(username: str):
    return await user_page.get_user(username)

@app.get("/users", tags=["User"])
async def get_all_users():
    return await user_page.get_all_users()

@app.post('/users', tags=["User"])
async def create_user(user_request: UsuarioCreate):
    return await user_page.create_user(user_request)

@app.put("/users/{username}", tags=["User"])
async def update_user(user_request: UsuarioBase, username: str):
    return await user_page.update_user(user_request, username)

@app.delete('/users/{username}', tags=["User"])
async def delete_user(username: str, password: str):
    return await user_page.delete_user(username, password)
#endregion

#Peticiones para las empresas
#region companies
@app.get("/company/{company}", tags=["Company"])
async def get_company(company: str):
    return await company_page.get_company(company)

@app.get("/company", tags=["Company"])
async def get_all_companies():
    return await company_page.get_all_companies()

@app.post("/company", response_model=CompanyResponse, tags=["Company"])
async def create_company(company_request: CompanyCreate):
    return await company_page.create_company(company_request)

@app.delete('/company/{company_name}', tags=["Company"])
async def delete_company(company: str):
    return await company_page.delete_company(company)
#endregion
                
#Peticiones para los descuentos
#region discounts

@app.get("/discount/{id}", tags=["Discount"])
async def get_discount(id: str):
    return await discounts_page.get_discount(id)

@app.get("/discounts/{company}", tags=["Discount"])
async def get_discount_name(company: str):
    return await discounts_page.get_discount_name(company)

@app.post("/discount/{company}", response_model=DiscountBase, tags=["Discount"])
async def create_discount(discount: DiscountCreate, company: str):
    return await discounts_page.create_discount(discount, company)

@app.delete("/discount/{id}", tags=["Discount"])
async def delete_discount(id: int):
    return await discounts_page.delete_discount(id)
#endregion

#Peticiones para los clientes
#region client

@app.get("/customer/{email}", tags=["Customer"])
async def get_customer(email: str):
    return await customer_page.get_customer_companies(email)

@app.get("/customers", tags=["Customer"])
async def get_all_customers():
    return await customer_page.get_all_customers()

@app.post("/customer/{company}", tags=["Customer"])
async def create_customer(request_customer: CustomerCreate, company: str, id: int):
    return await customer_page.create_customer(request_customer, company, id)

@app.delete("/customer/{email}", tags=["Customer"])
async def delete_customer(email: str):
    return await customer_page.delete_customer(email)
#endregion


#Peticiones para la caja
#region caja
@app.post("/abrir-caja", tags=["Caja"])
async def abrir_caja(request_caja: AbrirCajaBase):
    return await caja_page.abrir_caja(request_caja)


@app.post("/cerrar-caja/", tags=["Caja"])
async def cerrar_caja(username: str):
    return await caja_page.cerrar_caja(username)

#endregion 

#region transacciones

@app.post("/transaccion", tags=["Transacciones"])
async def transaccion(transaccion_data: TransaccionCreate, plan: str, email: Optional[str] = None):
    return transacciones_page.crear_transaccion(transaccion_data, plan, email)

@app.post("/num-transacciones/", tags=["Transacciones"])
async def transacciones(cierre_id):
    return transacciones_page.num_transacciones(cierre_id)

@app.post("/validar-descuento/", tags=["Transacciones"])
async def transacciones(email: str):
    return transacciones_page.validar_descuento(email)

#endregion

#Peticiones para configurar los planes de cobro
#region planes

@app.get("/plan/", tags=["Planes"])
async def get_plan(plan_name: str):
    return await plan_page.get_plan(plan_name)

@app.get("/plans/", tags=["Planes"])
async def get_all_plans():
    return await plan_page.get_all_plans()

@app.post('/planes/', tags=["Planes"])
async def create_plan(plan_request: PlanesCreate):
    return await plan_page.create_plan(plan_request)

@app.delete('/plan/', tags=["Planes"])
async def delete_plan(plan_name: str):
    return await plan_page.delete_plan(plan_name)

#endregion


#env\scripts\activate.bat
#uvicorn main:app --reload
#pip install peewee
#pip install mysql
#pip install sqlalchemy
#pip install bcrypt

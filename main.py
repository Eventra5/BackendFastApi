from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from database import DB as connection 
from database import User, Company, Discount, Customer, Customer_discount
from database import create_database

from schemas import CompanyResponse, UsuarioBase, UsuarioCreate, CompanyCreate, DiscountBase, DiscountCreate, CustomerCreate, UserLogin

import Pages.users as user_page
import Pages.companys as company_page
import Pages.discounts as discounts_page
import Pages.customers as customer_page
import Pages.login as login_page


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
    connection.create_tables([Customer])
    connection.create_tables([Customer_discount])


@app.on_event('shutdown')
def shutdown():

    if not connection.is_closed():
            connection.close()  

#endregion

#Peticiones para el login
#region login

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.post('/login')
async def login(request_login: OAuth2PasswordRequestForm = Depends()):
    return await login_page.login_user(request_login)
    

@app.get("/protected")
async def protected_routed(current_user: str = Depends(oauth2_scheme)):
    # La función de la ruta protegida solo se ejecuta si el token es válido
    # current_user contiene el usuario autenticado (token JWT)
    return {"message": "You have access to this protected route!"}

@app.get("/protectef")
async def protected_routed(current_user: str = Depends(oauth2_scheme)):
    # La función de la ruta protegida solo se ejecuta si el token es válido
    # current_user contiene el usuario autenticado (token JWT)
    return {"message": "You have access to this protected route!"}


#endregion


#Peticiones para los usuarios
#region users

@app.get("/userss/")
async def get_user(username: str, password: str):
    return await user_page.validate_user(username, password)

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

@app.get("/discounts/{company_name}")
async def get_discount_name(company_name: str):
    return await discounts_page.get_discount_name(company_name)

@app.post("/discount/{company_name}", response_model=DiscountBase)
async def create_discount(discount: DiscountCreate, company_name: str):
    return await discounts_page.create_discount(discount, company_name)

@app.delete("/discount/{discount_id}")
async def delete_discount(discount_id):
    return await discounts_page.delete_discount(discount_id)
#endregion

#Peticiones para los clientes
#region client

@app.get("/customer_company/{customer_email}")
async def get_customer(customer_email: str):
    return await customer_page.get_customer_companies(customer_email)

@app.get("/customers")
async def get_all_customers():
    return await customer_page.get_all_customers()

@app.post("/customer/{company_name}/{discount_id}")
async def create_customer(request_customer: CustomerCreate, company_name, discount_id):
    return await customer_page.create_customer(request_customer, company_name, discount_id)

@app.delete("/customer/{customer_email}")
async def delete_customer(customer_email: str):
    return await customer_page.delete_customer(customer_email)
#endregion


#endregion



#env\scripts\activate.bat
#uvicorn main:app --reload
#pip install peewee
#pip install mysql
#pip install sqlalchemy
#pip install bcrypt

from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime

#region Usuarios
class UsuarioBase(BaseModel):
    name: str
    last_name:str
    rol: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    password: str
    
class Usuario(UsuarioBase):
    id: int
    username: str
    salt: str
    fecha_registro: str

#endregion

#region Empresas
class CompanyBase(BaseModel):
    name: str = Field(..., max_length=50)
    tel: str
    email: EmailStr
    rfc: str
    cp: str
    domicilio: str


class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(BaseModel):
    name: str

#endregion

#region Descuentos
class DiscountBase(BaseModel):
    percentage: float = Field(..., gt=0, le=100)  # Porcentaje entre 0 y 100
    costo: float

class DiscountCreate(DiscountBase):
    pass

#endregion

#region clientes

class CustomerBase(BaseModel):
    name: str
    last_name: str
    email: EmailStr

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    fecha_inicio: date

#endregion

#region clientes con descuento

class CustomerBase_company(BaseModel):
    persona_id: int
    empresa_id: int
    descuento_id: int

class CustomerCompanyCreate(CustomerBase_company):
    pass

class CustomerCompany(CustomerBase_company):
    id: int

#endregion

#region Login
class UserLogin(BaseModel):
    username: str
    password: str

#endregion

#region Abrir caja

class AbrirCajaBase(BaseModel):
    cantidad_inicial: float
    username: str

class CrearCaja(AbrirCajaBase):
    pass

#endregion


#region suscripciones

class SuscripcionBase(BaseModel):
    username: str
    fecha_fin: str

class SuscripcioCreate(SuscripcionBase):
    pass

class Suscripcio(SuscripcionBase):
    id: int
    monto: float
    transaccion: str


#endregion

#region transacciones

class TransaccionBase(BaseModel):
    transaccion: str
    username: str
    fecha_expedicion: str

class TransaccionCreate(TransaccionBase):
    pass

class Transaccion(TransaccionBase):
    id: int
    monto: float

#endregion



#region Planes
class PlanesBase(BaseModel):
    plan: str
    cobro_base: float
    aumento: float


class PlanesCreate(PlanesBase):
    pass

class Planes(PlanesBase):
    id: int
#endregion

#region Config company
class MyCompanyBase(BaseModel):
    name: str
    logo: str

class MyCompanyCreate(MyCompanyBase):
    pass


#endregion 

#region Info company

class InfoCompanyBase(BaseModel):
    cp: str
    rfc: str
    tel: str
    name: str
    correo: EmailStr
    estado: str
    municipio: str
    domicilio: str

class InfoCompanyCreate(InfoCompanyBase):
    pass


#endregion
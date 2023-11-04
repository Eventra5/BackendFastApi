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

class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(BaseModel):
    name: str

#endregion

#region Descuentos
class DiscountBase(BaseModel):
    percentage: float = Field(..., gt=0, le=100)  # Porcentaje entre 0 y 100

class DiscountCreate(DiscountBase):
    pass

#endregion

#region clientes
class CustomerBase(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    fecha_fin: date


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
    fecha: datetime


class CrearCaja(AbrirCajaBase):
    pass


class TransaccionCreate(BaseModel):
    transaccion: str
    monto: float
    username: str

#endregion

#region Plan hora
class PlanesBase(BaseModel):
    name: str

class PlanesCreate(PlanesBase):
    pass
    
class Planes(PlanesBase):
    id: int



class PlanCobroBase(BaseModel):
    cobro_base: float
    cobro_hora: float

class PlanCobroCreate(PlanCobroBase):
    pass
    
class PlanCobro(PlanCobroBase):
    id: int
    
class Cobro(BaseModel):
    id: int
    plan: str
    cobro_base: float
    cobro_hora: float

#endregion
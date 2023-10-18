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
    start_date: datetime
    end_date: datetime

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

class UserLogin(BaseModel):
    username: str
    password: str

#region Abrir caja

class AbrirCajaBase(BaseModel):
    fecha: datetime
    cantidad_inicial: float

class CrearCaja(AbrirCajaBase):
    pass

#endregion


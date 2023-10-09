from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

#region Usuarios
class UsuarioBase(BaseModel):
    name: str
    rol: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    password: str
    
class Usuario(UsuarioBase):
    id: int
    fecha_registro: str

class updatepass(BaseModel):
    password: str

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
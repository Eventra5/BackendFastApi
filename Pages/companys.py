from database import Company, Discount

from peewee import DoesNotExist

from database import DB 

from schemas import CompanyCreate

from fastapi import HTTPException

async def get_company(company_get: str):
    company = Company.get_or_none(Company.name == company_get)

    if company:
        return company.__dict__["__data__"]
    else:
        raise HTTPException(status_code=404, detail=f"Empresa '{company_get}' no encontrado")

async def get_all_companies():
    company = list(Company.select())

    return [{"id": company.id, "name": company.name} for company in company]
    
async def create_company(company_request: CompanyCreate):


    if Company.select().where(Company.name == company_request.name).exists():
        raise HTTPException(status_code=400, detail="La empresa ya esta registrada")

    company = Company.create(
        name = company_request.name,
    )

    return company

async def delete_company(company_name):
    try:
        with DB.atomic():
            # Encuentra la empresa que deseas eliminar
            company = Company.get(Company.name == company_name)

            # Elimina los registros relacionados en la tabla Discount
            Discount.delete().where(Discount.company == company).execute()

            # Finalmente, elimina la empresa
            company.delete_instance()

            return {"mensaje": f"La empresa: '{company_name}' y sus registros relacionados eliminados exitosamente."}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="La empresa no existe.")
    except Exception as e:
        # Maneja cualquier otro error que pueda ocurrir durante la transacción
        raise HTTPException(status_code=500, detail="Error interno del servidor")


from database import DB 

from peewee import DoesNotExist

from fastapi import HTTPException

from schemas import CompanyCreate

from database import Company, Discount

async def get_company(company):

    company_info = Company.get_or_none(Company.name == company)

    if company_info:
        return company_info.__dict__["__data__"]
    else:
        raise HTTPException(status_code=404, detail=f"Empresa '{company}' no encontrado")

async def get_all_companies():

    company_info = list(Company.select())

    return [{"id": company.id, "name": company.name} for company in company_info]
    
async def create_company(company_request: CompanyCreate):


    if Company.select().where(Company.name == company_request.name).exists():
        raise HTTPException(status_code=400, detail="La empresa ya esta registrada")

    company = Company.create(
        name = company_request.name,
    )

    return company

async def delete_company(company):
    try:
        with DB.atomic():
            # Encuentra la empresa que deseas eliminar
            company_info = Company.get(Company.name == company)

            # Elimina los registros relacionados en la tabla Discount
            Discount.delete().where(Discount.company == company_info).execute()

            # Finalmente, elimina la empresa
            company_info.delete_instance()

            return {"mensaje": f"La empresa: '{company}' y sus registros relacionados eliminados exitosamente."}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="La empresa no existe.")
    except Exception as e:
        # Maneja cualquier otro error que pueda ocurrir durante la transacción
        raise HTTPException(status_code=500, detail="Error interno del servidor")


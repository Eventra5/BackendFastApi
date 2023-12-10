from database import Discount, Company

from peewee import DoesNotExist

from fastapi import HTTPException

async def get_discount(id):

    try:
        # Utiliza la relación 'discounts' para obtener los descuentos relacionados
        discounts = Discount.select().where(Discount.id == id)

        # Convierte los resultados en una lista de diccionarios
        discounts_list = [{"id": discount.id, "company": discount.company.name, "percentage": discount.percentage, "costo": discount.costo} for discount in discounts]

        return discounts_list
    
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="El descuento no existe.")
    except Exception as e:
            # Maneja cualquier otro error que pueda ocurrir
        raise HTTPException(status_code=500, detail="Error interno del servidor.")
    
async def get_discount_name(company_name: str):

    try:
        # Encuentra la empresa por su nombre
        company = Company.get(Company.name == company_name)

        # Utiliza la relación 'discounts' para obtener los descuentos relacionados
        discounts = Discount.select().where(Discount.company == company)

        # Convierte los resultados en una lista de diccionarios
        discounts_list = [{"id": discount.id, "company": discount.company.name, "percentage": discount.percentage, "costo": discount.costo} for discount in discounts]

        return discounts_list
    
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="La empresa no existe.")
    except Exception as e:
        # Maneja cualquier otro error que pueda ocurrir
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
async def get_all_discounts():

    discount_info = list(Discount.select())

    return [
        {
            "id": discount.id,
            "company_name": discount.company.name,
            "percentage": discount.percentage,
            "costo": discount.costo
        }
        for discount in discount_info
    ]

async def create_discount(discount, company_name):
    # Validar los datos de entrada utilizando Pydantic
    discount_data = discount.dict()
    
    try:
        # Obtener la empresa asociada al descuento por nombre
        company = Company.get(Company.name == company_name)
    except Company.DoesNotExist:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    # Crear el descuento en la base de datos y asociarlo a la empresa
    new_discount = Discount.create(company=company, **discount_data)
    return new_discount

async def delete_discount(id):

    discount = Discount.select().where((Discount.id == id)).first()

    if discount:
        discount.delete_instance()
        return {"mensaje": "Descuento eliminado con exito"}
    else:
        raise HTTPException(status_code=404, detail="El descuento no existe")
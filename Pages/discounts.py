from database import Discount, Company

from peewee import DoesNotExist

from schemas import DiscountCreate

from fastapi import HTTPException

async def get_discount(discount_id: str):

    try:

        # Utiliza la relación 'discounts' para obtener los descuentos relacionados
        discounts = Discount.select().where(Discount.id == discount_id)

        # Convierte los resultados en una lista de diccionarios
        discounts_list = [{"id": discount.id, "percentage": discount.percentage, "start_date": discount.start_date, "end_date": discount.end_date} for discount in discounts]

        return discounts_list
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="El descuento no existe.")
    except Exception as e:
            # Maneja cualquier otro error que pueda ocurrir
        raise HTTPException(status_code=500, detail="Error interno del servidor.")
    
async def get_discounts_by_company_name(company_name):
    try:
        # Encuentra la empresa por su nombre
        company = Company.get(Company.name == company_name)

        # Utiliza la relación 'discounts' para obtener los descuentos relacionados
        discounts = Discount.select().where(Discount.company == company)

        # Convierte los resultados en una lista de diccionarios
        discounts_list = [{"id": discount.id, "percentage": discount.percentage, "start_date": discount.start_date, "end_date": discount.end_date} for discount in discounts]

        return discounts_list
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="La empresa no existe.")
    except Exception as e:
        # Maneja cualquier otro error que pueda ocurrir
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
async def create_discount(discount: DiscountCreate, company_id: int):
    # Validar los datos de entrada utilizando Pydantic
    discount_data = discount.dict()
    
    # Obtener la empresa asociada al descuento
    company = Company.get_or_none(id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    
    # Crear el descuento en la base de datos y asociarlo a la empresa
    new_discount = Discount.create(company=company, **discount_data)
    return new_discount

async def delete_discount(discount_id):

    discount = Discount.select().where((Discount.id == discount_id)).first()

    if discount:
        discount.delete_instance()
        return {"mensaje": "Descuento eliminado con exito"}
    else:
        raise HTTPException(status_code=404, detail="El usuario no existe")
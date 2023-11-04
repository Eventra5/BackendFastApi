from database import Plan_fraccion, Plan_x_hora, Planes_cobro
from schemas import PlanCobroCreate
from fastapi import HTTPException

from peewee import DoesNotExist

async def create_plan_hora(plan_request: PlanCobroCreate, plan_name: str):
    # Validar los datos de entrada utilizando Pydantic
    plan_request_data = plan_request.dict()
    
    try:
        # Obtener la empresa asociada al descuento por nombre
        plan = Planes_cobro.get(Planes_cobro.name == plan_name)

    except Planes_cobro.DoesNotExist:
        raise HTTPException(status_code=404, detail="Plan de cobro no encontrado")

    # Crear el descuento en la base de datos y asociarlo a la empresa
    new_plan = Plan_x_hora.create(plan=plan, **plan_request_data)
    return new_plan

async def create_plan_fraccion(plan_request: PlanCobroCreate, plan_name: str):

    # Validar los datos de entrada utilizando Pydantic
    plan_request_data = plan_request.dict()
    
    try:
        # Obtener la empresa asociada al descuento por nombre
        plan = Planes_cobro.get(Planes_cobro.name == plan_name)

    except Planes_cobro.DoesNotExist:
        raise HTTPException(status_code=404, detail="Plan de cobro no encontrado")

    # Crear el descuento en la base de datos y asociarlo a la empresa
    new_plan = Plan_fraccion.create(plan=plan, **plan_request_data)
    return new_plan


async def get_all_cobros(plan_name):
    try:
        # Encuentra el plan de cobro que deseas obtener
        plan = Planes_cobro.get(Planes_cobro.name == plan_name)

        # Inicializa una lista vacía para almacenar los planes de cobro
        plan_list = []

        if Plan_x_hora.select().where(Plan_x_hora.plan == plan_name).exists():
            # Agrega los planes de cobro por hora a la lista
            plan_list.extend(list(Plan_x_hora.select().where(Plan_x_hora.plan == plan_name)))

        if Plan_fraccion.select().where(Plan_fraccion.plan == plan_name).exists():
            # Agrega los planes de cobro por fracción a la lista
            plan_list.extend(list(Plan_fraccion.select().where(Plan_fraccion.plan == plan_name)))

        # Convierte la lista de planes de cobro en una lista de diccionarios para la respuesta
        response_data = [
            {"id": plan.id, "plan": plan.plan.name, "cobro_base": plan.cobro_base, "cobro_hora": plan.cobro_hora}
            for plan in plan_list
        ]

        return response_data
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="El plan de cobro no existe.")

async def get_p_cobro(discount_id: str):

    try:

        if Plan_x_hora.select().where(Plan_x_hora.plan == plan_name).exists():
        
            Plan_x_hora.delete().where(Plan_x_hora.plan == plan).execute()


        # Utiliza la relación 'discounts' para obtener los descuentos relacionados
        discounts = Discount.select().where(Discount.id == discount_id)

        # Convierte los resultados en una lista de diccionarios
        discounts_list = [{"id": discount.id, "company": discount.company.name, "percentage": discount.percentage} for discount in discounts]

        return discounts_list
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="El descuento no existe.")
    except Exception as e:
            # Maneja cualquier otro error que pueda ocurrir
        raise HTTPException(status_code=500, detail="Error interno del servidor.")
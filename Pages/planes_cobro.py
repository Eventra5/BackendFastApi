from database import Plan_fraccion, Plan_x_hora, Planes_cobro

from fastapi import HTTPException

from peewee import DoesNotExist

from database import DB 

async def get_plan(plan_name):
    plan = Planes_cobro.get_or_none(Planes_cobro.name == plan_name)

    if plan:
        return plan.__dict__["__data__"]
    else:
        raise HTTPException(status_code=404, detail=f"Plan '{plan}' no encontrado")

async def get_all_plans():
    plan = list(Planes_cobro.select())

    return [{"id": plan.id, "name": plan.name} for plan in plan]

async def create_plan(plan_request):

    if Planes_cobro.select().where(Planes_cobro.name == plan_request.name).exists():
        raise HTTPException(status_code=400, detail="El plan de cobro ya esta registrado")
    
    plan = Planes_cobro.create(
        name = plan_request.name,
    )

    return 'Plan creado con exito'

async def delete_plan(plan_name):
    try:
        with DB.atomic():
            
            # Encuentra la empresa que deseas eliminar
            plan = Planes_cobro.get(Planes_cobro.name == plan_name)

            if Plan_x_hora.select().where(Plan_x_hora.plan == plan_name).exists():
        
                Plan_x_hora.delete().where(Plan_x_hora.plan == plan).execute()

            if Plan_fraccion.select().where(Plan_fraccion.plan == plan_name).exists():

                Plan_fraccion.delete().where(Plan_fraccion.plan == plan).execute()

            plan.delete_instance()

            return {"mensaje": f"El plan: '{plan_name}' y sus registros relacionados eliminados exitosamente."}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="El plan no existe.")
    except Exception as e:
        # Maneja cualquier otro error que pueda ocurrir durante la transacción
        raise HTTPException(status_code=500, detail="Error interno del servidor")


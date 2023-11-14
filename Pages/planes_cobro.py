from database import Planes_cobro

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

    return [{"ID": plan.id, "Plan": plan.plan, "Cobro base": plan.cobro_base, 'Aumento': plan.aumento} for plan in plan]

async def create_plan(plan_request):

    if Planes_cobro.select().where(Planes_cobro.plan == plan_request.plan).exists():
        raise HTTPException(status_code=400, detail="El plan de cobro ya esta registrado")
    
    plan = Planes_cobro.create(
        plan = plan_request.plan,
        cobro_base = plan_request.cobro_base,
        aumento = plan_request.aumento
    )

    return 'Plan creado con exito'

async def delete_plan(plan_name):

    try:

        plan = Planes_cobro.select().where((Planes_cobro.plan == plan_name)).first()

        if plan:
            plan.delete_instance()
            return {"mensaje": "Plan eliminado con exito"}
        else:
            raise HTTPException(status_code=404, detail="El plan no existe")
        
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Plan no encontrada")


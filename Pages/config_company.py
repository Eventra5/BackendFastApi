from database import InfoCompanyWeb, InfoCompanyLegal

from fastapi import HTTPException


async def get_info_web():
    company = list(InfoCompanyWeb.select())

    return [{"id": company.id,"name": company.name, "logo": company.logo} for company in company]

async def create_info_web(request_company):


    if InfoCompanyWeb.select().where(InfoCompanyWeb.name == request_company.name).exists():
        raise HTTPException(status_code=400, detail="Los datos ya estan registrados")

    company = InfoCompanyWeb.create(
        name = request_company.name,
        logo = request_company.logo,
    )

    return {"mensaje": "Info creada exitosamente"}

async def update_info_web(request_company, id):

    company = InfoCompanyWeb.get_or_none(InfoCompanyWeb.id == id)

    if company:
        # Actualiza los campos del usuario con los valores proporcionados
        company.name = request_company.name
        company.logo = request_company.logo
        company.save()
        return {"mensaje": "Datos actualizados exitosamente"}
    else:
        raise HTTPException(status_code=404, detail=f"ID: '{id}' no encontrado")
    
async def delete_info_web(id):

    company = InfoCompanyWeb.select().where(InfoCompanyWeb.id == id).first()

    if company:
        company.delete_instance()
        return {"mensaje": "Datos borrados exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="El id no existe")
    

async def get_info_legal():
    company = list(InfoCompanyLegal.select())

    return [
        {
            "id": company.id, 
            "cp": company.cp, 
            "rfc": company.rfc,
            "tel": company.tel,
            "name": company.name,
            "correo": company.correo,
            "estado": company.estado,
            "municipio": company.municipio,
            "domicilio": company.domicilio,
        } 

        for company in company]

async def create_info_legal(request_company):

    if InfoCompanyLegal.select().where(InfoCompanyLegal.name == request_company.name).exists():
        raise HTTPException(status_code=400, detail="Los datos ya estan registrados")

    company = InfoCompanyLegal.create(

        cp = request_company.cp,
        rfc = request_company.rfc,
        tel = request_company.tel,
        name = request_company.name,
        correo = request_company.correo,
        estado = request_company.estado,
        municipio = request_company.municipio,
        domicilio = request_company.domicilio,

    )

    return {"mensaje": "Info creada exitosamente"}

async def update_info_legal(request_company, id):

    company = InfoCompanyLegal.get_or_none(InfoCompanyLegal.id == id)

    if company:
        # Actualiza los campos del usuario con los valores proporcionados
        company.cp = request_company.cp
        company.rfc = request_company.rfc
        company.tel = request_company.tel
        company.name = request_company.name
        company.correo = request_company.correo
        company.estado = request_company.estado
        company.municipio = request_company.municipio
        company.domicilio = request_company.domicilio
        company.save()

        return {"mensaje": "Datos actualizados exitosamente"}
    else:
        raise HTTPException(status_code=404, detail=f"ID: '{id}' no encontrado")
    
async def delete_info_legal(id):

    company = InfoCompanyLegal.select().where(InfoCompanyLegal.id == id).first()

    if company:
        company.delete_instance()
        return {"mensaje": "Datos borrados exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="El id no existe")
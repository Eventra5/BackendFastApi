from database import Info_parking

from fastapi import HTTPException

######################################################

async def get_info_parking(id):

    parking = Info_parking.get_or_none(Info_parking.id == id)

    if parking:
        return parking.__dict__["__data__"]
    else:
        raise HTTPException(status_code=404, detail=f"El id parking '{id}' no fue encontrado")


# Comentarios aca bien sinseros bien esquizos
async def get_all_parkings():

    Parking = list(Info_parking.select())

    return [{"id": parkin.id, "name": parkin.rfc, "email": parkin.nombre, "username": parkin.domicilio, "password": parkin.codigo_postal, "password": parkin.email, "password": parkin.tel} for parkin in Parking]

async def create_info(request_parking):

    datos = Info_parking.create(
        rfc= request_parking.rfc,
        nombre= request_parking.nombre,
        domicilio= request_parking.domicilio,
        estado= request_parking.estado,
        codigo_postal= request_parking.codigo_postal,
        email= request_parking.email,
        tel= request_parking.tel,
    )

    return datos

async def update_info(request_parking, codigo):

    info = Info_parking.get_or_none(Info_parking.codigo_postal == codigo)

    if info:
        
        rfc= request_parking.rfc,
        nombre= request_parking.nombre,
        domicilio= request_parking.domicilio,
        estado= request_parking.estado,
        codigo_postal = request_parking.codigo,
        email= request_parking.email,
        tel= request_parking.tel,
        info.save()

        return {"mensaje": "Datos del estacionamiento actualizados exitosamente"}

# COmentarios aca bien locos bien maquiavelos
async def delete_user(id):

    parking = Info_parking.select().where((Info_parking.id == id)).first()

    if parking:
        parking.delete_instance()
        return {"mensaje": f"La informacion del parking '{id}' fue eliminado exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="La informacion del estacionamiento no existe")

    

#/
# 
# 
# 
#/    raise HTTPException(status_code=404, detail="La informacion del estacionamiento no existe")



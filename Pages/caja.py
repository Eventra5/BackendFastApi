from database import AperturaCaja, CierreCaja, User, Transacciones
from database import Plan_fraccion, Plan_x_hora, Planes_cobro

from MySQLdb import IntegrityError

from fastapi import HTTPException

from schemas import CrearCaja

from datetime import datetime, timedelta

def obtener_id_apertura_caja():
    try:
        # Buscar la última apertura de caja que no tiene cierre asociado
        apertura = AperturaCaja.select().where(AperturaCaja.estado == True).order_by(AperturaCaja.id.desc()).get()
        return apertura.id
    
    except AperturaCaja.DoesNotExist:
        return None  # No se encontró una apertura de caja sin cierre

def transacciones(cierre_id):
    # Buscar el rango de transacciones utilizando el ID de cierre de caja
    num_transacciones = Transacciones.select().join(CierreCaja, on=(Transacciones.apertura_caja == CierreCaja.apertura_caja)).where(CierreCaja.id == cierre_id).count()

    return num_transacciones

async def abrir_caja(request_caja: CrearCaja):

    # Verifica que el usuario de apertura exista
    user_exists = User.select().where(User.username == request_caja.username).exists()

    if not user_exists:
        raise HTTPException(status_code=404, detail="El usuario de apertura no existe")
    
    ultima_apertura = AperturaCaja.select().where(AperturaCaja.estado == True).order_by(AperturaCaja.fecha.desc()).first()

    if ultima_apertura:
        raise HTTPException(status_code=400, detail="Ya existe una apertura de caja. Debes cerrarla primero.")
    
    # Continúa con la creación de la fila en la tabla AperturaCaja
    try:
        abrir_caja = AperturaCaja.create(
            usuario_apertura = request_caja.username,
            cantidad_inicial = 1000.0,
            fecha = datetime.now(),
            estado=True  # Marca la apertura como activa
        )

    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Error al abrir caja")

    return {"message": "Caja abierta con éxito"}

async def cerrar_caja(username):

    # Verificar si existe una apertura de caja activa
    ultima_apertura = AperturaCaja.select().where(AperturaCaja.estado == True).order_by(AperturaCaja.fecha.desc()).first()
    if not ultima_apertura:
        raise HTTPException(status_code=400, detail="No existe una caja abierta para cerrar.")
    
    #Calculamos la cantidad final provisionalmente
    cantidad_final = 1200.0  #Establecemos el valor de la cantidad final
    diferencia = cantidad_final - ultima_apertura.cantidad_inicial
    
    # Registrar el cierre de caja
    cierre = CierreCaja.create(
        fecha=datetime.now(),
        cantidad_final=cantidad_final,
        diferencia=diferencia,
        usuario_cierre=username,  # Asegúrate de obtener el usuario actual
        apertura_caja=ultima_apertura,  # Vincula el cierre a la apertura correspondiente
    )
    
    # Marcar la apertura de caja como cerrada
    ultima_apertura.estado = False
    ultima_apertura.save()
    
    return {"message": "Caja cerrada con éxito."}


def crear_transaccion(transaccion_data, plan_name, plan_id):

    plan = Planes_cobro.get(Planes_cobro.name == plan_name)

    if Plan_x_hora.select().where(Plan_x_hora.plan == plan).exists():
        # Agrega los planes de cobro por hora a la lista
        plan_info = Plan_x_hora.get(Plan_x_hora.id == plan_id)



    id_caja = obtener_id_apertura_caja()

    try:
        # Verifica que la apertura de caja exista y está relacionada con el usuario
        transaccion = Transacciones.create(
            transaccion=transaccion_data.transaccion,
            monto=transaccion_data.monto,
            fecha=datetime.now(),
            user=transaccion_data.username,
            apertura_id=id_caja
        )

        return {"message": "Transacción creada exitosamente"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def corbro_x_hora(plan_name, plan_id):
    try:
        plan = Planes_cobro.get(Planes_cobro.name == plan_name)

        if Plan_x_hora.select().where(Plan_x_hora.plan == plan).exists():
            # Agrega los planes de cobro por hora a la lista
            plan_info = Plan_x_hora.get(Plan_x_hora.id == plan_id)

        fecha_expedicion = '2023-11-03 13:46:01'  # Asegúrate de que la hora tenga dos dígitos en el formato (02 en lugar de 2)

        # Convertir la fecha de expedición en un objeto datetime
        fecha_expedicion = datetime.strptime(fecha_expedicion, "%Y-%m-%d %H:%M:%S")

        # Obtener la hora actual del sistema
        now = datetime.now()

        # Calcular la diferencia en horas y minutos entre la fecha de expedición y la fecha de fin
        diferencia = now - fecha_expedicion

        print(fecha_expedicion)
        print(now)
        print(diferencia)
   
        # Calcular el costo basado en la tarifa de $20 por la primera hora
        costo = plan_info.cobro_base
        aumento = plan_info.cobro_hora

        # Si la diferencia es mayor que una hora, agregar $10 por cada hora adicional
        if diferencia > timedelta(hours=1):
            horas_adicionales = diferencia.total_seconds() / 3600 - 1  # Resta 1 hora base
            costo += aumento * horas_adicionales

        return {"costo": costo}
    except ValueError:
        return {"error": "Formato de fecha incorrecto. Utiliza el formato 'YYYY-MM-DD HH:MM:SS'"}
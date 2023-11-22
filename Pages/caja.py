from database import AperturaCaja, CierreCaja, User

from MySQLdb import IntegrityError

from fastapi import HTTPException

from schemas import CrearCaja

from datetime import datetime
    
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

<<<<<<< HEAD
<<<<<<< Updated upstream
def crear_transaccion(transaccion_data, plan_name):
=======
def transacciones(cierre_id):
    # Buscar el rango de transacciones utilizando el ID de cierre de caja
    num_transacciones = Transacciones.select().join(CierreCaja, on=(Transacciones.apertura_caja == CierreCaja.apertura_caja)).where(CierreCaja.id == cierre_id).count()

    return num_transacciones

def crear_transaccion(transaccion_data):
>>>>>>> Stashed changes
=======
>>>>>>> efb9367c178e5f0ae0c28bb07ea95fb6925f0eff

    id_caja = obtener_id_apertura_caja()

    try:
        if id_caja is None:
            raise HTTPException(status_code=400, detail="No hay una caja abierta actualmente. Abra una caja para realizar transacciones.")
        
        calcular_monto = cobros.funciones_por_plan.get(plan_name)

        if calcular_monto:
            monto = calcular_monto(plan_name)

            transaccion = Transacciones.create(
                transaccion=transaccion_data.transaccion,
                monto=monto,
                fecha=datetime.now(),
                user=transaccion_data.username,
                apertura_id=id_caja
            )

            return {"message": "Transacción creada exitosamente"}
        else:
            raise HTTPException(status_code=400, detail="Plan no encontrado o sin función asociada")
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


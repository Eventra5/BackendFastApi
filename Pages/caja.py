from database import AperturaCaja, CierreCaja, User, Transacciones

from MySQLdb import IntegrityError

from fastapi import HTTPException

from schemas import CrearCaja

from datetime import datetime

def obtener_id_apertura_caja():
    try:
        # Buscar la última apertura de caja que no tiene cierre asociado
        apertura = AperturaCaja.select().where(AperturaCaja.estado == True).order_by(AperturaCaja.id.desc()).get()
        return apertura.id
    
    except AperturaCaja.DoesNotExist:
        return None  # No se encontró una apertura de caja sin cierre

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

def transacciones(cierre_id):
    # Buscar el rango de transacciones utilizando el ID de cierre de caja
    num_transacciones = Transacciones.select().join(CierreCaja, on=(Transacciones.apertura_caja == CierreCaja.apertura_caja)).where(CierreCaja.id == cierre_id).count()

    return num_transacciones


def crear_transaccion(transaccion_data):

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
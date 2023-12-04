from database import AperturaCaja, CierreCaja, User, Transacciones

from MySQLdb import IntegrityError

from fastapi import HTTPException

from schemas import CrearCaja

from datetime import datetime

from peewee import fn

###############################################################################

def Calcular_total(id: int):
    try:
        total_montos = Transacciones.select(fn.SUM(Transacciones.monto)).where(
            Transacciones.apertura_caja == id
        ).scalar()

        total_redondeado = round(total_montos, 2) if total_montos is not None else 0.0

        return total_redondeado
    
    except Transacciones.DoesNotExist:
        return 0.0

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
            cantidad_inicial = request_caja.cantidad_inicial,
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
    
    total_cobros = Calcular_total(ultima_apertura)
    cantidad_final = total_cobros + ultima_apertura.cantidad_inicial

    diferencia = cantidad_final - ultima_apertura.cantidad_inicial
    diferencia = round(diferencia, 2)

    
    # Registrar el cierre de caja
    cierre = CierreCaja.create(
        fecha=datetime.now(),
        cantidad_final=cantidad_final,
        diferencia=diferencia,
        usuario_cierre=username,  # Asegúrate de obtener el usuario actual
        apertura_caja=ultima_apertura,  # Vincula el cierre a la apertura correspondiente
    )
    
    fecha_formateada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cierre_data = {
        "fecha": fecha_formateada,
        "cantidad_final": cierre.cantidad_final,
        "cantidad_inicial": ultima_apertura.cantidad_inicial,
        "ganancia": cierre.diferencia,
    }

    # Marcar la apertura de caja como cerrada
    ultima_apertura.estado = False
    ultima_apertura.save()
    
    return cierre_data

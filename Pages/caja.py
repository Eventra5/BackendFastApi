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

def Calcular_total_suscripcion(id: int):
    try:

        total_montos_suscripcion = Transacciones.select(fn.SUM(Transacciones.monto)).where(
            (Transacciones.apertura_caja == id) & (Transacciones.transaccion == 'suscripcion')
        ).scalar()

        total_redondeado_suscripcion = round(total_montos_suscripcion, 2) if total_montos_suscripcion is not None else 0.0

        return total_redondeado_suscripcion
    
    except Transacciones.DoesNotExist:
        return 0.0
    
def Calcular_total_dia(id: int):
    try:

        total_montos_dia = Transacciones.select(fn.SUM(Transacciones.monto)).where(
            (Transacciones.apertura_caja == id) & (Transacciones.transaccion == 'cobro plan dia')
        ).scalar()

        total_redondeado_dia= round(total_montos_dia, 2) if total_montos_dia is not None else 0.0

        return total_redondeado_dia
    
    except Transacciones.DoesNotExist:
        return 0.0
    
def Calcular_total_fraccion(id: int):
    try:

        total_montos_fraccion = Transacciones.select(fn.SUM(Transacciones.monto)).where(
            (Transacciones.apertura_caja == id) & (Transacciones.transaccion == 'cobro plan fraccion')
        ).scalar()

        total_redondeado_fraccion= round(total_montos_fraccion, 2) if total_montos_fraccion is not None else 0.0

        return total_redondeado_fraccion
    
    except Transacciones.DoesNotExist:
        return 0.0
    
def Calcular_total_hora(id: int):
    try:

        total_montos_hora = Transacciones.select(fn.SUM(Transacciones.monto)).where(
            (Transacciones.apertura_caja == id) & (Transacciones.transaccion == 'cobro plan hora')
        ).scalar()

        total_redondeado_hora = round(total_montos_hora, 2) if total_montos_hora is not None else 0.0

        return total_redondeado_hora
    
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

async def cerrar_caja(request_caja, username):

    # Verificar si existe una apertura de caja activa
    ultima_apertura = AperturaCaja.select().where(AperturaCaja.estado == True).order_by(AperturaCaja.fecha.desc()).first()

    if not ultima_apertura:
        raise HTTPException(status_code=400, detail="No existe una caja abierta para cerrar.")
    
    total_cobros = Calcular_total(ultima_apertura)

    cantidad_final = total_cobros + ultima_apertura.cantidad_inicial
    cantidad_final = round(cantidad_final, 2)

    ingresos = cantidad_final - ultima_apertura.cantidad_inicial
    ingresos = round(ingresos, 2)

    dia = Calcular_total_dia(ultima_apertura)

    hora = Calcular_total_hora(ultima_apertura)

    fraccion = Calcular_total_fraccion(ultima_apertura)

    suscripciones = Calcular_total_suscripcion(ultima_apertura)

    if request_caja.cantidad_inicial != ultima_apertura.cantidad_inicial or request_caja.ingresos != ingresos:

        mensaje_error = f"Existe un error con el monto inicial declarado : {request_caja.cantidad_inicial}, o con los ingresos: {request_caja.ingresos}"
        raise HTTPException(status_code=400, detail=mensaje_error)

    # Registrar el cierre de caja
    cierre = CierreCaja.create(
        fecha=datetime.now(),
        cantidad_final=cantidad_final,
        ingresos = ingresos,
        suscripciones = suscripciones,
        dia = dia,
        hora = hora,
        fraccion = fraccion,
        usuario_cierre=username,  # Asegúrate de obtener el usuario actual
        apertura_caja=ultima_apertura,  # Vincula el cierre a la apertura correspondiente
    )
    
    fecha_formateada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cierre_data = {
        "fecha": fecha_formateada,
        "cantidad_final": cierre.cantidad_final,
        "cantidad_inicial": ultima_apertura.cantidad_inicial,
        "ingresos": cierre.ingresos,
        "suscripciones": suscripciones,
        "cobros_dia": dia,
        "cobros_hora": hora,
        "cobros_fraccion": fraccion,
    }

    # Marcar la apertura de caja como cerrada
    ultima_apertura.estado = False
    ultima_apertura.save()
    
    return cierre_data

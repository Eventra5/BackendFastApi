from database import AperturaCaja, CierreCaja ,Transacciones, Customer_discount, Customer
from datetime import datetime, date
from fastapi import HTTPException
import Pages.cobros as cobros



def validar_descuento(email: str):

    if not email:
        return None 
    
    fecha_actual = date.today()

    try:

        customer = Customer.get(Customer.email == email)

        if not customer.descuento:
            raise HTTPException(status_code=400, detail="No hay descuento asociado")

        descuento_cliente = Customer_discount.get(Customer_discount.customer == customer)

        fecha_inicio = descuento_cliente.fecha_inicio
        fecha_fin = descuento_cliente.fecha_fin

        if fecha_actual < fecha_inicio or fecha_actual > fecha_fin:
            customer.descuento = False
            customer.save()  # Guardar el cambio en la base de datos
            descuento_cliente.delete_instance()
            raise HTTPException(status_code=400, detail="El descuento ya expiró")
        
        else: 

            return descuento_cliente.descuento.percentage

    except Customer_discount.DoesNotExist:
        return None  # No se encontró descuento asociado al cliente

    

def obtener_id_apertura_caja():
    try:
        # Buscar la última apertura de caja que no tiene cierre asociado
        apertura = AperturaCaja.select().where(AperturaCaja.estado == True).order_by(AperturaCaja.id.desc()).get()
        return apertura.id
    
    except AperturaCaja.DoesNotExist:
        return None  # No se encontró una apertura de caja sin cierre

def num_transacciones(cierre_id):
    # Buscar el rango de transacciones utilizando el ID de cierre de caja
    num_transacciones = Transacciones.select().join(CierreCaja, on=(Transacciones.apertura_caja == CierreCaja.apertura_caja)).where(CierreCaja.id == cierre_id).count()

    return num_transacciones

def crear_transaccion(transaccion_data, plan_name, email):

    try:
        
        id_caja = obtener_id_apertura_caja()
        descuento = validar_descuento(email)

        print(descuento)

        if descuento is False:
            raise HTTPException(status_code=400, detail="El descuento ya expiro")
        
        if id_caja is None:
            raise HTTPException(status_code=400, detail="No hay una caja abierta actualmente. Abra una caja para realizar transacciones.")
        

        if plan_name in cobros.funciones_por_plan:
            # Obtiene la función correspondiente al plan
            calcular_monto = cobros.funciones_por_plan[plan_name]

            # Calcula el costo utilizando la función seleccionada
            monto = calcular_monto(plan_name, descuento)
            print(monto)

        else:
            raise HTTPException(status_code=400, detail="Plan no encontrado o sin función asociada")
        
        transaccion = Transacciones.create(

            transaccion=transaccion_data.transaccion,
            monto=monto,
            fecha=datetime.now(),
            user=transaccion_data.username,
            apertura_id=id_caja
        )

        return {"message": f"Transacción creada exitosamente {'/n'} el monto es: {monto}"}

    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        

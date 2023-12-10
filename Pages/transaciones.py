from database import AperturaCaja, CierreCaja ,Transacciones, CustomerDiscount, Customer, User, Discount
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

        descuento_cliente = CustomerDiscount.get(CustomerDiscount.customer == customer)

        fecha_inicio = descuento_cliente.fecha_inicio
        fecha_fin = descuento_cliente.fecha_fin

        if fecha_actual < fecha_inicio or fecha_actual > fecha_fin:
            customer.descuento = False
            customer.save()  # Guardar el cambio en la base de datos
            descuento_cliente.delete_instance()
            raise HTTPException(status_code=400, detail="El descuento ya expiró")
        
        else: 

            return descuento_cliente.descuento.percentage

    except CustomerDiscount.DoesNotExist:
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

        if descuento is False:
            raise HTTPException(status_code=400, detail="El descuento ya expiro")
        
        if id_caja is None:
            raise HTTPException(status_code=400, detail="No hay una caja abierta actualmente. Abra una caja para realizar transacciones.")
        

        if plan_name in cobros.funciones_por_plan:
            # Obtiene la función correspondiente al plan
            calcular_monto = cobros.funciones_por_plan[plan_name]

            # Calcula el costo utilizando la función seleccionada
            monto = calcular_monto(transaccion_data.fecha_expedicion, plan_name, descuento)

        else:
            raise HTTPException(status_code=400, detail="Plan no encontrado o sin función asociada")
        
        print(monto)
        
        transaccion = Transacciones.create(

            transaccion=transaccion_data.transaccion,
            monto=monto,
            fecha=datetime.now(),
            user=transaccion_data.username,
            apertura_id=id_caja
        )
        
        return monto

    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
def transaccion_suscripcion(transaccion_data, id, email):

    try:
        
        id_caja = obtener_id_apertura_caja()
        
        if id_caja is None:
            raise HTTPException(status_code=400, detail="No hay una caja abierta actualmente. Abra una caja para realizar transacciones.")
        
        if not Customer.select().where(Customer.email == email).exists():
            raise HTTPException(status_code=404, detail="El cliente no existe")
        
        if not User.select().where(User.username == transaccion_data.username).exists():
            raise HTTPException(status_code=404, detail="El usuario no existe")
        
        plan_name = "suscripcion"

        if plan_name in cobros.funciones_por_plan:

            calcular_monto = cobros.funciones_por_plan[plan_name]

            monto = calcular_monto(id)

        else:
            raise HTTPException(status_code=400, detail="Plan no encontrado o sin función asociada")
        
        transaccion = Transacciones.create(

            transaccion="suscripcion",
            monto=monto,
            fecha=datetime.now(),
            user=transaccion_data.username,
            apertura_id=id_caja
        )

        # Obtener la empresa y el descuento existentes
        customer = Customer.get(Customer.email == email)
        discount = Discount.get(Discount.id == id)

        customer.descuento = True
        customer.save()  # Guardar el cambio en la base de datos


        CustomerDiscount.create(
            customer=customer,
            company=discount.company,
            descuento=discount.id,
            fecha_inicio = date.today(),
            fecha_fin = transaccion_data.fecha_fin
        )


        return monto


    except User.DoesNotExist as e:
        raise HTTPException(status_code=404, detail=f"El username: {transaccion_data.username} no fue encontrado")
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
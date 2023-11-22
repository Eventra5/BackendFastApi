from typing import Optional

from database import Planes_cobro

from datetime import datetime, timedelta

def cobro_fraccion(plan_name: str, descuento: Optional[float] = None):

    plan_info = Planes_cobro.get(Planes_cobro.name == plan_name)
    costo_base = plan_info.costo_base
    costo_hora = plan_info.costo_hora

    try:
        fecha_expedicion = '2023-11-03 13:46:01'  # Asegúrate de que la hora tenga dos dígitos en el formato (02 en lugar de 2)

        # Convertir la fecha de expedición en un objeto datetime
        fecha_expedicion = datetime.strptime(fecha_expedicion, "%Y-%m-%d %H:%M:%S")

        # Obtener la hora actual del sistema
        now = datetime.now()

        # Calcular la diferencia en horas y minutos entre la fecha de expedición y la fecha de fin
        diferencia = now - fecha_expedicion

        # Si la diferencia es mayor que una hora, agregar $10 por cada hora adicional
        if diferencia > timedelta(hours=1):
            horas_adicionales = diferencia.total_seconds() / 3600 - 1  # Resta 1 hora base
            costo_base += costo_hora * horas_adicionales

        # Aplicar el descuento si se proporciona
        if descuento is not None:
            costo_base -= (costo_base * descuento) / 100  # Aplicar el descuento

        costo = round(costo_base, 2)
        return costo
    except ValueError:
        return {"error": "Formato de fecha incorrecto. Utiliza el formato 'YYYY-MM-DD HH:MM:SS'"}

def cobro_hora(plan_name: str, descuento: Optional[float] = None):

    plan_info = Planes_cobro.get(Planes_cobro.plan == plan_name)
    costo_base = plan_info.cobro_base
    aumento = plan_info.aumento

    fecha_expedicion = '2023-11-03 13:46:01'  
    fecha_expedicion = datetime.strptime(fecha_expedicion, "%Y-%m-%d %H:%M:%S")

    try:
        
        # Obtener la hora actual del sistema
        fecha_fin = datetime.now()

        # Calcular la diferencia en horas y minutos entre la fecha de expedición y la fecha de fin
        diferencia = (fecha_fin - fecha_expedicion).total_seconds() / 3600
        diferencia = int(diferencia)
 
        costo_base = costo_base + aumento * max(0, diferencia - 1)

        # Aplicar el descuento si se proporciona
        if descuento is not None:
            costo_base -= (costo_base * descuento) / 100  # Aplicar el descuento

        costo = round(costo_base, 2)
        return costo
    except ValueError:
        return {"error": "Formato de fecha incorrecto. Utiliza el formato 'YYYY-MM-DD HH:MM:SS'"}
    
def cobro_dia(plan_name: str, descuento: Optional[float] = None):

    print (descuento)
    
    try:
        # Obtener información del plan desde la base de datos
        plan_info = Planes_cobro.get(Planes_cobro.plan == plan_name)
        costo_base = plan_info.cobro_base
        aumento = plan_info.aumento

        # Obtener la fecha de expedición (simulada para propósitos de demostración)
        fecha_expedicion_str = '2023-11-03 13:46:01'  # Formato: 'YYYY-MM-DD HH:MM:SS'
        fecha_expedicion = datetime.strptime(fecha_expedicion_str, "%Y-%m-%d %H:%M:%S")

        # Obtener la fecha y hora actuales del sistema
        now = datetime.now()

        # Calcular la diferencia entre la fecha actual y la fecha de expedición en segundos
        diferencia_segundos = (now - fecha_expedicion).total_seconds()

        # Convertir los segundos en días y horas
        dias_transcurridos = diferencia_segundos // (24 * 3600)
        horas_restantes = (diferencia_segundos % (24 * 3600)) // 3600

        # Calcular el costo basado en la tarifa diaria y tarifa por hora adicional
        costo_base = costo_base * dias_transcurridos + aumento * horas_restantes

        if descuento is not None:
            costo_base -= (costo_base * descuento) / 100  # Aplicar el descuento

        costo = round(costo_base, 2)
        return costo
    
    except Planes_cobro.DoesNotExist:
        return {"error": f"El plan '{plan_name}' no fue encontrado"}
    except ValueError as e:
        return {"error": str(e)}  # Manejar errores de conversión de fecha
    except Exception as e:
        return {"error": str(e)}  # Capturar y manejar otros errores
    
funciones_por_plan = {
    "hora": cobro_hora,
    "fracccion": cobro_fraccion,
    "dia": cobro_dia,
}
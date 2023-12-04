from typing import Optional

from database import Planes_cobro

from fastapi import HTTPException

from datetime import datetime, timedelta

def cobro_fraccion(fecha_expedicion: str, plan_name: str, descuento: Optional[float] = None):

    try:

<<<<<<< HEAD
        plan_info = Planes_cobro.get(Planes_cobro.name == plan_name)
        costo_base = plan_info.costo_base
        costo_hora = plan_info.costo_hora

        fecha_expedicion = '2023-12-01 19:06:01'  # Asegúrate de que la hora tenga dos dígitos en el formato (02 en lugar de 2)
=======
        plan_info = Planes_cobro.get(Planes_cobro.plan == plan_name)
        costo_base = plan_info.cobro_base
        costo_hora = plan_info.aumento
>>>>>>> 9bb55c8584e9f249c2609acab1f067bae85514bc

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

    except Planes_cobro.DoesNotExist as e:
        raise HTTPException(status_code=404, detail=f"El plan '{plan_name}' no fue encontrado")
    
    except ValueError as e:
        return {"error": str(e)}  # Manejar errores de conversión de fecha
    except Exception as e:
        return {"error": str(e)}  # Capturar y manejar otros errores

def cobro_hora(fecha_expedicion: str, plan_name: str, descuento: Optional[float] = None):

    try:
        
        plan_info = Planes_cobro.get(Planes_cobro.plan == plan_name)
        costo_base = plan_info.cobro_base
        aumento = plan_info.aumento

<<<<<<< HEAD
        fecha_expedicion = '2023-12-01 20:16:01'
=======
>>>>>>> 9bb55c8584e9f249c2609acab1f067bae85514bc
        fecha_expedicion = datetime.strptime(fecha_expedicion, "%Y-%m-%d %H:%M:%S")

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
    
    except Planes_cobro.DoesNotExist as e:
        raise HTTPException(status_code=404, detail=f"El plan '{plan_name}' no fue encontrado")
    
    except ValueError as e:
        return {"error": str(e)}  # Manejar errores de conversión de fecha
    except Exception as e:
        return {"error": str(e)}  # Capturar y manejar otros errores
    
def cobro_dia(fecha_expedicion: str, plan_name: str, descuento: Optional[float] = None):

    try:
        # Obtener información del plan desde la base de datos
        plan_info = Planes_cobro.get(Planes_cobro.plan == plan_name)

        costo_base = plan_info.cobro_base
        aumento = plan_info.aumento

<<<<<<< HEAD
        # Obtener la fecha de expedición (simulada para propósitos de demostración)
        fecha_expedicion_str = '2023-11-30 20:28:01' 
        fecha_expedicion = datetime.strptime(fecha_expedicion_str, "%Y-%m-%d %H:%M:%S")
=======
        fecha_expedicion = datetime.strptime(fecha_expedicion, "%Y-%m-%d %H:%M:%S")
>>>>>>> 9bb55c8584e9f249c2609acab1f067bae85514bc

        # Obtener la fecha y hora actuales del sistema
        now = datetime.now()

        # Calcular la diferencia entre la fecha actual y la fecha de expedición en segundos
        diferencia_segundos = (now - fecha_expedicion).total_seconds()

        # Convertir los segundos en días y horas
        dias_transcurridos = diferencia_segundos // (24 * 3600)
        horas_restantes = (diferencia_segundos % (24 * 3600)) // 3600

        # Verificar si han pasado los días y aplicar el aumento
        if dias_transcurridos > 0:
            costo_base += aumento * dias_transcurridos

        if descuento is not None:
            costo_base -= (costo_base * descuento) / 100  # Aplicar el descuento

        costo = round(costo_base, 2)
        return costo    

    except Planes_cobro.DoesNotExist as e:
        raise HTTPException(status_code=404, detail=f"El plan '{plan_name}' no fue encontrado")
    
    except ValueError as e:
        return {"error": str(e)}  # Manejar errores de conversión de fecha
    except Exception as e:
        return {"error": str(e)}  # Capturar y manejar otros errores

funciones_por_plan = {
    "hora": cobro_hora,
    "fraccion": cobro_fraccion,
    "dia": cobro_dia,
}
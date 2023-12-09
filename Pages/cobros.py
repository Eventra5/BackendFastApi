from typing import Optional

from database import PlanesCobro

from fastapi import HTTPException

from datetime import datetime, timedelta

def cobro_fraccion(fecha_expedicion: str, plan_name: str, descuento: Optional[float] = None):

    try:
        
        plan_info = Planes_cobro.get(Planes_cobro.plan == plan_name)
        costo_base = plan_info.cobro_base
        costo_hora = plan_info.aumento

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
        plan_info = PlanesCobro.get(PlanesCobro.plan == plan_name)

        costo_base = plan_info.cobro_base
        aumento = plan_info.aumento

        fecha_expedicion = datetime.strptime(fecha_expedicion, "%Y-%m-%d %H:%M:%S")

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

    except PlanesCobro.DoesNotExist as e:
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
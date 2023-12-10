from MySQLdb import IntegrityError, OperationalError
from database import Customer, CustomerDiscount, Company, Discount, DB

from peewee import DoesNotExist

from fastapi import HTTPException

from datetime import date

import Email.Enviar_Qr as Enviar_Qr

import Pages.transaciones as transaccion_suscripcion

async def get_customer_companies(customer_email: str):
    try:
        # Obtener los registros de Customer_company para un cliente específico
        customer_companies = CustomerDiscount.select().where(CustomerDiscount.customer_email == customer_email)
        customer = Customer.select().where(Customer.email == customer_email)

        results1 = [
            {
                "name": cc1.name,
                "last_name": cc1.last_name,
                "customer_email": cc1.email,  # Acceder al objeto Customer y luego al atributo email
            }
            for cc1 in customer
        ]
        
        if Customer.select().where(Customer.descuento == 1):
            results2 = [
                {
                    "discount_id": cc.descuento.id,
                    "company": cc.company.name,
                    "percentage": cc.descuento.percentage,
                }
                for cc in customer_companies
            ]
        else:
            results2 = []
            
        # Combinar los resultados en un solo arreglo
        combined_results = results1 + results2
        
        return combined_results
    
    except Customer.DoesNotExist:
        raise HTTPException(status_code=404, detail="El cliente no existe")
    
async def get_all_customers():
    customer = list(Customer.select())

    return [{"id": customer.id, "name": customer.name, "last name": customer.last_name, "email": customer.email} for customer in customer]

async def create_customer(request_customer):

    try:

        # Verificar si el correo electrónico ya está en uso
        if Customer.select().where(Customer.email == request_customer.email).exists():
            raise HTTPException(status_code=400, detail="El correo electrónico ya está en uso")
        
        customer = Customer.create(
            name= request_customer.name,
            last_name= request_customer.last_name,
            email= request_customer.email,
        )

        return {"message": "Cliente creado y asociado con éxito"}

    except Company.DoesNotExist:
        raise HTTPException(status_code=404, detail="La empresa no existe")

    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Error de integridad de la base de datos: {str(e)}")

    except OperationalError as e:
        raise HTTPException(status_code=500, detail=f"Error de operación de base de datos: {str(e)}")

async def delete_customer(customer_email: str):

    try:
        with DB.atomic():
            # Encuentra el cliente que deseas eliminar
            customer = Customer.get(Customer.email == customer_email)

            # Elimina los registros relacionados en la tabla Customer_company
            CustomerDiscount.delete().where(CustomerDiscount.customer == customer).execute()

            # Finalmente, elimina el cliente
            customer.delete_instance()

            return {"mensaje": f"El cliente: '{customer_email}' y sus registros relacionados eliminados exitosamente."}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="El cliente no existe.")
    except Exception as e:
        # Maneja cualquier otro error que pueda ocurrir durante la transacción
        raise HTTPException(status_code=500, detail="Error interno del servidor")








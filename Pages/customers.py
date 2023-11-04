from MySQLdb import IntegrityError, OperationalError
from database import Customer, Customer_discount, Company, Discount, DB

from peewee import DoesNotExist

from fastapi import HTTPException

from datetime import date

import Email.Enviar_Qr as Enviar_Qr

async def get_customer_companies(customer_email: str):
    try:
        # Obtener los registros de Customer_company para un cliente específico
        customer_companies = Customer_discount.select().where(Customer_discount.customer_email == customer_email)
        
        # Crear una lista de resultados como diccionarios
        results = [
            {
                "id": cc.id,
                "customer_email": cc.customer.email,  # Acceder al objeto Customer y luego al atributo email
                "company_name": cc.company.name,  # Acceder al objeto Company y luego al atributo name
                "discount": {
                    "id": cc.descuento.id,
                    "percentage": cc.descuento.percentage,
                    "start_date": cc.descuento.start_date.strftime("%d-%m-%Y"),
                    "end_date": cc.descuento.end_date.strftime("%d-%m-%Y"),
                },
            }
            for cc in customer_companies
        ]
        
        return results
    
    except Customer.DoesNotExist:
        raise HTTPException(status_code=404, detail="El cliente no existe")
    
async def get_all_customers():
    customer = list(Customer.select())

    return [{"id": customer.id, "name": customer.name, "last name": customer.last_name, "email": customer.email} for customer in customer]

async def create_customer(request_customer, company_name, discount_id):
    try:

        fecha_actual = date.today()
        fecha_iniciof = fecha_actual.strftime("%d/%m/%Y")

        company = Company.get(Company.name == company_name)

        # Verificar si el correo electrónico ya está en uso
        if Customer.select().where(Customer.email == request_customer.email).exists():
            raise HTTPException(status_code=400, detail="El correo electrónico ya está en uso")
        
        if not Discount.select().where(Discount.company == company).exists():
            raise HTTPException(status_code=404, detail="El descuento no existe")
        
        if not Discount.select().where(Discount.id == discount_id).exists():
            raise HTTPException(status_code=404, detail="El descuento no existe")
        
        customer = Customer.create(
            name=request_customer.name,
            last_name=request_customer.last_name,
            email= request_customer.email,
        )
        
        # Obtener la empresa y el descuento existentes
        customer = Customer.get(Customer.email == request_customer.email)
        company = Company.get(Company.name == company_name)
        discount = Discount.get_by_id(discount_id)


        Customer_discount.create(
            customer=customer,
            company=company,
            descuento=discount,
            fecha_inicio = fecha_iniciof,
            fecha_fin = request_customer.fecha_fin
        )

        Enviar_Qr.send_email(request_customer.email)

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
            Customer_discount.delete().where(Customer_discount.customer == customer).execute()

            # Finalmente, elimina el cliente
            customer.delete_instance()

            return {"mensaje": f"El cliente: '{customer_email}' y sus registros relacionados eliminados exitosamente."}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="El cliente no existe.")
    except Exception as e:
        # Maneja cualquier otro error que pueda ocurrir durante la transacción
        raise HTTPException(status_code=500, detail="Error interno del servidor")








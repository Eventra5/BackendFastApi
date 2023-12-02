from email.mime.image import MIMEImage

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from peewee import DoesNotExist

from fastapi import HTTPException

from database import Customer

import Qr.Qr_personalized as Qr_personalized_page

def data_customer(customer_email):

    try:

        customer = Customer.get(Customer.email == customer_email)

        # Ahora puedes utilizar los datos para generar el código QR
        data = f"""{customer.email}"""

        return data

    except DoesNotExist:
        raise HTTPException(status_code=404, detail="El cliente no existe")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

def send_email(email):

    data_client = data_customer(email)
    Qr_cliente = Qr_personalized_page.generate_qr_code(data_client)

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'soporte.tareas.uas@gmail.com'
    smtp_password = 'jzan laoo ckre zonr'

    # Crear un objeto SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)

    # Iniciar la conexión segura
    server.starttls()

    # Iniciar sesión en el servidor
    server.login(smtp_username, smtp_password)

    # Crear el mensaje
    subject = 'Qr estacionamiento'
    from_email = smtp_username
    to_email = email
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject

    # Cuerpo del correo
    body = 'Gracias por formar parte de esta empresa, acontinuacion se le adjuntara un Qr para tener descuentos en el estacionamiento.'
    message.attach(MIMEText(body, 'plain'))

    # Adjuntar una imagen (en este caso, el código QR)
    image = Qr_cliente
    attachment = MIMEImage(image.read(), name='codigo_qr.png')
    message.attach(attachment)

    # Enviar el correo
    server.sendmail(from_email, to_email, message.as_string())

    # Cerrar la conexión
    server.quit()



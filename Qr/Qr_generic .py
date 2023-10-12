import qrcode
import datetime

# Obtiene la fecha y hora actual
fecha_hora_actual = datetime.datetime.now()

# Convierte la fecha y hora en una cadena de texto
fecha_hora_str = fecha_hora_actual.strftime('%d-%m-%Y %I:%M %p')

# Crea el código QR con la fecha y hora
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(fecha_hora_str)
qr.make(fit=True)

# Crea una imagen del código QR
img = qr.make_image(fill_color="black", back_color="white")

# Guarda la imagen en un archivo
img.save("codigo_qr.png")

# Imprime la fecha y hora para referencia
print("Fecha y Hora:", fecha_hora_str)
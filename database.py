from peewee import *
from datetime import datetime

from peewee import DoesNotExist

import mysql.connector

DB = MySQLDatabase(
    'estacionamiento',
    user = 'root',
    password = 'dali12345',
    host = 'localhost',
    port = 3306
)

class User(Model):
    id = AutoField()
    username = CharField(max_length=6, unique= True)
    password = CharField(max_length=10, unique=True)
    name = CharField()
    last_name = CharField()
    email = CharField()
    salt = CharField() 
    rol = CharField(max_length=5)
    fecha_de_registro = DateField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    def __str__(self):
        return self.name
    
    class Meta:
        database = DB
        table_name = 'users'

class Company(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        database = DB
        table_name = 'companies'

class Discount(Model):
    id = AutoField()
    company = ForeignKeyField(Company, backref='discount_company', column_name='company_name', to_field='name')
    percentage = FloatField()

    def __str__(self):
        return self.company
    
    class Meta:
        database = DB
        table_name = 'discounts'

class Customer(Model):
    id = AutoField()
    name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    email = CharField(max_length=100, unique=True)


    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        database = DB
        table_name = 'customers'

class Customer_discount(Model):
    
    customer = ForeignKeyField(Customer, backref='customer_companies', column_name='customer_email', to_field='email')
    company = ForeignKeyField(Company, backref='company_customers', column_name='company_name', to_field='name')
    descuento = ForeignKeyField(Discount)
    fecha_inicio = DateField()
    fecha_fin = DateField()

    class Meta:
        database = DB
        table_name = 'customer_discount'

# Define el modelo de "abrir caja"
class AperturaCaja(Model):
    fecha = DateTimeField()
    cantidad_inicial = FloatField()
    usuario_apertura = ForeignKeyField(User, backref='aperturas_de_caja', column_name='opening_user', to_field='username')
    
    class Meta:
        database = DB

# Define el modelo de "cierre de caja"
class CierreCaja(Model):
    fecha = DateTimeField()
    cantidad_final = FloatField()
    diferencia = FloatField()
    usuario_cierre = ForeignKeyField(User, backref='cierres_de_caja', column_name='close_user', to_field='name')
    apertura_caja = ForeignKeyField(AperturaCaja, backref='cierres_de_caja', null=True)  # Clave foránea que referencia la apertura de caja

    class Meta:
        database = DB




def create_database(nombre_base_de_datos):

    config = {
        'user': 'root',
        'password': 'dali12345',
        'host': 'localhost',
        'port': 3306,
    }

    try:
        # Crear una conexión temporal
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Crear la base de datos si no existe
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {nombre_base_de_datos}")

        # Cerrar la conexión temporal
        cursor.close()
        connection.close()

        # Reabrir la conexión utilizando la base de datos recién creada
        config['database'] = nombre_base_de_datos
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        return connection, cursor

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None, None




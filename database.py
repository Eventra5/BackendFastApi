from peewee import *
from datetime import datetime
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
    name = CharField(max_length=50)
    password = CharField(max_length=10, unique=True)
    rol = CharField(max_length=5)
    email = CharField(max_length=100, unique=True)
    fecha_de_registro = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

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
    start_date = DateField()
    end_date = DateField()

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

class Customer_company(Model):
    
    customer = ForeignKeyField(Customer, backref='customer_companies', column_name='customer_email', to_field='email')
    company = ForeignKeyField(Company, backref='company_customers', column_name='company_name', to_field='name')
    descuento = ForeignKeyField(Discount)

    class Meta:
        database = DB
        table_name = 'customer_company'




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




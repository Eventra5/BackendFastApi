from peewee import *
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
    rol = CharField(max_length=5, constraints=[Check('rol IN (\'admin\', \'user\')')])
    fecha_registro = CharField()

    def __str__(self):
        return self.name
    
    class Meta:
        database = DB
        table_name = 'users'

class Company(Model):
    id = AutoField(primary_key=True)
    cp = CharField(max_length=5)
    tel = CharField(max_length=20)
    rfc = CharField(max_length=13)
    name = CharField(max_length=50, unique=True)
    email = CharField()
    domicilio = CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        database = DB
        table_name = 'companies'

class Discount(Model):
    id = AutoField()
    company = ForeignKeyField(Company, backref='discount_company', column_name='company_name', to_field='name')
    percentage = FloatField()
    costo = FloatField()


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
    descuento = BooleanField(default=False)


    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        database = DB
        table_name = 'customers'

class CustomerDiscount(Model):
    
    customer = ForeignKeyField(Customer, backref='customer_companies', column_name='customer_email', to_field='email', unique=True)
    company = ForeignKeyField(Company, backref='company_customers', column_name='company_name', to_field='name')
    descuento = ForeignKeyField(Discount)
    fecha_inicio = DateField()
    fecha_fin = DateField()

    class Meta:
        database = DB
        table_name = 'customer_discount'

class AperturaCaja(Model):
    id = AutoField()
    cantidad_inicial = FloatField()
    usuario_apertura = ForeignKeyField(User, backref='apertura_de_caja', column_name='usuario_apertura', to_field='username')
    fecha = DateTimeField()
    estado = BooleanField(default=True)
    
    class Meta:
        database = DB
        table_name = 'box_open'

class CierreCaja(Model):
    id = AutoField()
    cantidad_final = FloatField()
    ingresos = FloatField()
    suscripciones = FloatField()
    dia = FloatField()
    hora = FloatField()
    fraccion = FloatField()
    usuario_cierre = ForeignKeyField(User, backref='cierres_de_caja', column_name='usuario_cierre', to_field='username')
    apertura_caja = ForeignKeyField(AperturaCaja, backref='cierres_de_caja', null=True)
    fecha = DateTimeField()

    class Meta:
        database = DB
        table_name = 'box_close'

class Transacciones(Model):
    transaccion = CharField()
    monto = FloatField()
    fecha = DateTimeField()
    user = ForeignKeyField(User, backref='usuario_transaccion', column_name='user', to_field='username')
    apertura_caja = ForeignKeyField(AperturaCaja, backref='transacciones', column_name='apertura_id')

    class Meta:
        database = DB
        table_name = 'transacciones'

class PlanesCobro(Model):
    id = AutoField()
    plan = CharField(unique= True)
    cobro_base = FloatField()
    aumento = FloatField(null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        database = DB
        table_name = 'planes_cobro'

class InfoCompanyWeb(Model):

    id = AutoField(primary_key=True)
    name = CharField(max_length=50, unique=True)
    logo = CharField(max_length=255, null=True) 


    class Meta:
        database = DB
        table_name = 'info_company'

class InfoCompanyLegal(Model):

    id = AutoField(primary_key=True)
    cp = CharField(max_length=5)
    rfc = CharField(max_length=13)
    tel = CharField(max_length=20)
    name = CharField(max_length=50)
    correo = CharField(max_length=50)
    estado = CharField(max_length=20)
    municipio = CharField(max_length=20)
    domicilio = CharField(max_length=100)

    class Meta:
        database = DB
        table_name = 'info_company_legal'

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




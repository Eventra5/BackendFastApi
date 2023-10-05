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
    name = CharField(max_length=50)
    password = CharField(max_length=10, unique=True)
    rol = CharField(max_length=5)
    email = CharField(max_length=100, unique=True)
    fecha_de_registro = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    def __str__(self):
        return self.name
    
    class Meta:
        database = DB
        table_nam = 'users'

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




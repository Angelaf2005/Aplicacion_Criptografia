import sqlite3
import hashlib
import os


# Crear la base de datos
def create_db():

    if not os.path.exists('DataBase'):
        os.mkdir('DataBase')

    if not os.path.exists('DataBase/DataBase.db'):

        # Conectarse a la base de datos (creara un archivo si no existe)
        conexion = sqlite3.connect('DataBase/DataBase.db')
        # Crear un cursor
        cursor = conexion.cursor()

        #Crear una tabla si no existe
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            user TEXT NOT NULL,
                            email TEXT NOT NULL,
                            pass_hash TEXT NOT NULL
                        )''')
    
        # Guardar los cambios y cerrar la conexión
        conexion.commit()
        conexion.close()
    else:
        #No hacer nada
        pass
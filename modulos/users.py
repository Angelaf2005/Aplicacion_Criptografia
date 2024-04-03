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


# Verificar inicio de sesion de un usuario
def login(user, password):
    # Conectarse a la base de datos
    conexion = sqlite3.connect('DataBase/DataBase.db')
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para seleccionar el usuario con el nombre dado
    cursor.execute("SELECT * FROM usuarios WHERE user = ?", (user,))
    usuario = cursor.fetchone()

    # Verificar si el usuario existe
    if usuario:
        # Calcular el hash de la contraseña proporcionada
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Verificar si la contraseña coincide
        if usuario[2] == password_hash:
            print('Inicio de sesión exitoso')
            return True
        else:
            print('La contraseña es incorrecta')
            return False
    else:
        print('El usuario no existe')
        return False




# Registro de un usuario en la base de datos
def register(name, user, email, password):

    #Conectarse a la base de datos
    conexion = sqlite3.connect('DataBase/DataBase.db')
    cursor = conexion.cursor()
    
    # Ejecutar una consulta SQL para verificar si el usuario ya existe
    cursor.execute("SELECT * FROM usuarios WHERE user = ?", (user,))
    usuario_x_usuario = cursor.fetchone()

    # Ejecutar una consulta SQL para verificar si el email ya existe
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    usuario_x_email = cursor.fetchone()

    # Verificar si el usuario ya existe por el nombre de usuario
    if usuario_x_usuario:
        print('Este nombre de usuario ya existe.')

    # Verificar si el usuario ya existe por el email
    elif usuario_x_email:
        print("Este email ya esta registrado.")
    # Si pasa las verificaciones, regitrar el nuevo usuario
    else:

        #Calcular el hash de la contraseña proporcionada
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Datos del nuevo usuario
        new_user = (name, user, email, password_hash)

        # Insertar el nuevo usuario en la tabla
        cursor.execute("INSERT INTO usuarios (name, user, email, pass_hash) VALUES (?, ?, ?, ?)", new_user)

        # Guardar los cambios y cerrar la conexión
        conexion.commit()
        conexion.close()
        
        print('Registrado')
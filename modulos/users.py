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
        if usuario[4] == password_hash:
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




# Verificar si el correo existe para envio de codigo
def email_exist(email):
    # Conectarse a la base de datos
    conexion = sqlite3.connect('DataBase/DataBase.db')
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para verificar si el email existe
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    user = cursor.fetchone

    # Cerrar la conexion
    conexion.close()

    #Verificar si se encontro algun usuario con el email dado.
    if user:
        return True
    else:
        return False




# Mosificar base de datos para cambio de contraseña
def modify_db(email, password):

    # Calcular el hash de la nueva contraseña proporcionada
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    print(password_hash)

    # Conectarse con la base de datos
    conexion = sqlite3.connect('DataBase/DataBase.db')
    cursor = conexion.cursor()

    # Ejecutar consulta SQL para actualizar el hash de la contraseña
    cursor.execute("UPDATE usuarios SET pass_hash = ? WHERE email = ?", (password_hash, email))

    # Guardar los cambios y Cerrar la conexión
    conexion.commit()
    conexion.close()
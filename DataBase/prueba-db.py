import sqlite3


# Conectarse a la base de datos (creará un archivo si no existe)
conexion = sqlite3.connect('DataBase.db')
# Crear un cursor
cursor = conexion.cursor()

# Crear una tabla, si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY,
                    user TEXT NOT NULL,
                    pass_hash TEXT NOT NULL
                 )''')

# Guardar los cambios y cerrar la conexión
conexion.commit()
conexion.close()





# Datos del usuario
user = 'Raul'
passw = 'Hash1'




# Conectarse a la base de datos
conexion = sqlite3.connect('DataBase.db')
cursor = conexion.cursor()

# Ejecutar una consulta SQL para seleccionar todos los usuarios
cursor.execute("SELECT * FROM usuarios")

# Recuperar los resultados
usuarios = cursor.fetchall()

for usuario in usuarios:
    if usuario[1] == user:
        print('El usuario ya existe')
    else:
        print('El usuario no existe - Registrando')

        # Datos del nuevo usuario
        nuevo_usuario = (user, passw)

        # Insertar el nuevo usuario en la tabla
        cursor.execute("INSERT INTO usuarios (user, pass_hash) VALUES (?, ?)", nuevo_usuario)




# Cerrar la conexión
conexion.close()




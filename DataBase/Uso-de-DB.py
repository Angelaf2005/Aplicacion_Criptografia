import sqlite3



# ------ CREAR UNA TABLA -----

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









# ------ AGREGAR CONTENIDO A LA BASE DE DATOS ------

# Conectarse a la base de datos
conexion = sqlite3.connect('DataBase.db')
cursor = conexion.cursor()

# Datos del nuevo usuario
nuevo_usuario = ('Raul', 'Hash1')

# Insertar el nuevo usuario en la tabla
cursor.execute("INSERT INTO usuarios (user, pass_hash) VALUES (?, ?)", nuevo_usuario)

# Guardar los cambios y cerrar la conexión
conexion.commit()
conexion.close()










# ------ CONSULTAR INFORMACIÓN A LA BASE DE DATOS -------

# CONSULTAR TODA UNA COLUMNA

# Conectarse a la base de datos
conexion = sqlite3.connect('DataBase.db')
cursor = conexion.cursor()

# Ejecutar una consulta SQL para seleccionar todos los usuarios
cursor.execute("SELECT * FROM usuarios")

# Recuperar los resultados
usuarios = cursor.fetchall()

# Mostrar los resultados en pantalla
for usuario in usuarios:
    print("ID:", usuario[0])
    print("Nombre:", usuario[1])
    print("Contraseña:", usuario[2])
    print()

# Cerrar la conexión
conexion.close()








# CONSULTAR INFORMACIÓN EN ESPECIFICO


# Conectarse a la base de datos
conexion = sqlite3.connect('DataBase.db')
cursor = conexion.cursor()

# Definir el nombre de usuario que quieres buscar
nombre_usuario = 'Alice'

# Ejecutar una consulta SQL para seleccionar la información del usuario con el nombre especificado
cursor.execute("SELECT * FROM usuarios WHERE user = ?", (nombre_usuario,))

# Recuperar los resultados
usuarios = cursor.fetchall()

# Mostrar los resultados en pantalla
for usuario in usuarios:
    print("ID:", usuario[0])
    print("Nombre:", usuario[1])
    print("Contraseña:", usuario[2])
    print()

# Cerrar la conexión
conexion.close()






# ------ ELIMINAR CONTENIDO DE LA BASE DE DATOS ------

# Conectarse a la base de datos
conexion = sqlite3.connect('DataBase.db')
cursor = conexion.cursor()

# Nombre del usuario que quieres eliminar
nombre_usuario = 'Alice'

# Ejecutar una consulta SQL para eliminar el usuario específico
cursor.execute("DELETE FROM usuarios WHERE user = ?", (nombre_usuario,))

# Guardar los cambios y cerrar la conexión
conexion.commit()
conexion.close()

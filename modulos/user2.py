from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import hashlib
import os
from flask_login import UserMixin
class User(UserMixin):
    def __init__(self,id,name,username,email,password) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.name = name
        self.email = email
    @classmethod
    def check_pass(self,password_hash,password):
        return check_password_hash(password_hash,password)
class ModelUser():
    @classmethod
    def login(self,user, password):
        # Conectarse a la base de datos
        conexion = sqlite3.connect('DataBase/DataBase.db')
        cursor = conexion.cursor()
        # Ejecutar una consulta SQL para seleccionar el usuario con el nombre dado
        cursor.execute("SELECT * FROM usuarios WHERE user = ?", (user,))
        usuario = cursor.fetchone()
        # Verificar si el usuario existe
        if usuario:
            userconection = User(usuario[0],usuario[1],usuario[2],usuario[3],User.check_pass(usuario[4],userconection.password))
            return userconection
        else:
            print('El usuario no existe')
            return False
    @classmethod
    def register(self,name, user, email, password):
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
            password_hash = generate_password_hash(password)
            # Datos del nuevo usuario
            new_user = (name, user, email, password_hash)
            # Insertar el nuevo usuario en la tabla
            cursor.execute("INSERT INTO usuarios (name, user, email, pass_hash) VALUES (?, ?, ?, ?)", new_user)
            # Guardar los cambios y cerrar la conexión
            conexion.commit()
            cursor.execute("SELECT * FROM usuarios WHERE user = ?", (user,))
            a = cursor.fetchone()
            userconection = User(a[0],name,user,email,password_hash)
            print('Registrado')
            return userconection
    @classmethod
    def get_by_id(self,id):
        # Conectarse a la base de datos
        conexion = sqlite3.connect('DataBase/DataBase.db')
        cursor = conexion.cursor()
        # Ejecutar una consulta SQL para seleccionar el usuario con el nombre dado
        cursor.execute("SELECT id, name, user, email FROM usuarios WHERE id = {}".format(id))
        usuario = cursor.fetchone()
        # Verificar si el usuario existe
        if usuario:
            return User(usuario[0],usuario[1],usuario[2],usuario[3],None)
        else:
            print('El usuario no existe')
            return False
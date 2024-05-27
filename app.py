from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory, send_file,jsonify
from modulos import eckeys, users, fernet, RSA, user2,Cesar
from flask_login import login_user,login_required,UserMixin,LoginManager,current_user, logout_user
from os import urandom, path
import os
import time
from werkzeug.utils import secure_filename

#app
app = Flask(__name__)
UPLOAD_FOLDER = "/Uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_manager = LoginManager(app)

# Generar clave de sesion
app.secret_key = urandom(32)

@login_manager.user_loader
def load_user(user_id):
    return user2.ModelUser.get_by_id(int(user_id))

@app.route("/")
def principal_page():
    return render_template("index.html")

@app.route("/login",  methods=["GET","POST"])
def login():
    # Si se envian datos al servidor
    if request.method == "POST":
        # Formulario de inicio de sesion
        cer = request.files["archivo_cer"]
        key = request.files["archivo_key"]
        passw = request.form["password"]
        # Seguridad en los nombres de archivos
        filenamecer = secure_filename(cer.filename)
        filenamekey = secure_filename(key.filename)
        # Guarda los archivos en el servidor en /Uploads
        cer.save("Uploads/"+filenamecer)
        key.save("Uploads/"+filenamekey)
        try:
            # Con la contraseña, desencriptar el archivo .key y verificar el certificado
            validate = eckeys.verify_certificate("Uploads/"+filenamecer, "Uploads/"+filenamekey, passw)
            # SI el certificado es valido
            if validate == True:
            # Obtener los datos del certificado
                name,username,email = eckeys.read_user_certificate("Uploads/"+filenamecer)
                if username != None:
                    # Verificar si el usuario existe en la base de datos
                    userconection = user2.ModelUser.login(username,passw)
                    # SI el usuario existe en la base de datos
                    if userconection != None and userconection!=False:
                        # Crear una sesion de usuario
                        login_user(userconection)
                        time.sleep(0.3)
                        # Redirigirlo a sus notas
                        return redirect(url_for('nota'))
                    else:
                        return render_template('Form.html')
        except Exception as e:
            return redirect(url_for("principal_page"))
    else:
        return render_template('Form.html')
    
@app.route("/notas", methods=["GET","POST"])
@login_required
def nota():
    print(current_user.password)
    if request.method == "POST":
        nota = request.form["nota"]
        encript = request.form["criptografia"]
        if encript == "fernet":
            fernet.save_note(nota,current_user.username)
        elif encript == "rsa":
            RSA.save_notes(nota,current_user.username,current_user.password)
        elif encript == "cesar":
            Cesar.save_note(nota,current_user.username)
        return render_template("notas.html")
    return render_template("notas.html")

@app.route("/integrantes")
def integrantes():
    return render_template("integrantes.html")


@app.route("/verlasnotas",methods=['POST','GET'])
@login_required
def notasg():
    if request.method == "POST":
        enc = request.form["metodo"]
        if (enc == "Notas Fernet"):
            mensaje = fernet.fernet_decrypt(current_user.username)
            return render_template('Nguardadas.html',mensaje=mensaje)
        elif(enc == "Notas césar"):
            mensaje = Cesar.cesar_decrypt(current_user.username)
        elif(enc == 'Mensaje encriptado césar'):
            mensaje = Cesar.read_encrypted_cesar_notes(current_user.username)
        elif (enc == "Mensaje Encriptado Fernet"):
            mensaje = fernet.read_encrypted_messages(current_user.username)
        elif (enc == 'Notas RSA'):
            mensaje = RSA.rsa_decrypt(current_user.username,current_user.password)
        elif (enc == 'Mensaje encriptado RSA'):
            mensaje = RSA.read_encrypted_notes(current_user.username)
        return render_template('Nguardadas.html',mensaje=mensaje)
    return render_template('Nguardadas.html')

@app.route("/register", methods=["GET","POST"])
def register():
    # Si se envian datos al servidor
    if request.method == "POST":
        # Formulario de registro
        user = request.form["usuario"]
        passwd = request.form["passwd"]
        email = request.form["email"]
        name = request.form["name"]
        # Crear la base de datos si no existe
        users.create_db()
        # Registrar al usuario
        userconection = user2.ModelUser.register(name,user,email,passwd)
        # Si se registro con exito
        if userconection != None:
            # Crear sesion de usuario
            login_user(userconection)
            print(current_user.password)
            # Generar las claves por primera vez
            fernet.fernet_key_generator(user)
            eckeys.keys_generator(name, user, passwd, email)
            RSA.rsa_key_generator(current_user.username,current_user.password)
            #rsa.rsa_key_generator(user, passwd)
            # Redirigirlo a descargar sus archivos
            return redirect(url_for("uploads",nombre=user))
        return render_template("registro.html")
    return render_template("registro.html")

# Cerrar sesion
@login_required
@app.route('/logout', methods=['GET'])
def logout():
    logout(current_user)
    return redirect(url_for("principal_page"))

@app.route('/uploads/<string:nombre>')
@login_required
def uploads(nombre=""):
    if nombre == "" or nombre != current_user.username:
        return redirect("/")
    else:
        return render_template("archivos.html",archivo=nombre)
    
@login_required
@app.route("/PrivateKey/<string:archivo>")
def PrivateKey(archivo=""):
    if archivo == "" or archivo != current_user.username:
        return (redirect("/"))
    else:
        var = archivo+"_encrypted_private_key.key"
        return send_file("Data/ECDSA/Private-Keys/"+var)
    
@login_required
@app.route("/PublicKey/<string:archivo>")
def Certificate(archivo=""):
    if archivo == "" or archivo != current_user.username:
        return (redirect("/"))
    else:
        var = archivo+"_Certificate.cer"
        return send_file("Data/ECDSA/Certificates/"+var)
    

if __name__ == "__main__":
    app.run() # host='0.0.0.0'
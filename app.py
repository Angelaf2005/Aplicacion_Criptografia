from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory, send_file
from modulos import eckeys, users, fernet, rsa, restore, user2
from flask_login import login_user,login_required,UserMixin,LoginManager,current_user
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
    if request.method == "POST":
        cer = request.files["archivo_cer"]
        key = request.files["archivo_key"]
        passw = request.form["password"]
        filenamecer = secure_filename(cer.filename)
        filenamekey = secure_filename(key.filename)
        cer.save("Uploads/"+filenamecer)
        key.save("Uploads/"+filenamekey)
        try:
            name,username,email = eckeys.read_user_certificate("Uploads/"+filenamecer)
            if username != None:
                userconection = user2.ModelUser.login(username,passw)
                if userconection != None and userconection!=False:
                    login_user(userconection)
                    time.sleep(0.3)
                    return redirect(url_for('nota'))
                else:
                    return render_template('Form.html')
        except:
            return redirect(url_for("principal_page"))
    else:
        return render_template('Form.html')
@app.route("/notas", methods=["GET","POST"])
@login_required
def nota(mensaje="No hay notas guardadas"):
    if request.method == "POST":
        nota = request.form["nota"]
        encript = request.form["criptografia"]
        if encript == "fernet":
            fernet.save_note(nota,current_user.username)
        return render_template("notas.html",mensaje=fernet.fernet_decrypt(current_user.username))
    return render_template("notas.html",mensaje=fernet.fernet_decrypt(current_user.username))   
@app.route("/integrantes")
def integrantes():
    return render_template("integrantes.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        user = request.form["usuario"]
        passwd = request.form["passwd"]
        email = request.form["email"]
        name = request.form["name"]
        users.create_db()
        userconection = user2.ModelUser.register(name,user,email,passwd)
        if userconection != None:
            login_user(userconection)
            fernet.fernet_key_generator(user)
            eckeys.keys_generator(name, user, passwd, email)
            #rsa.rsa_key_generator(user, passwd)
            print(current_user)
            return redirect(url_for("uploads",nombre=user))
        return render_template("registro.html")
    return render_template("registro.html")
@app.route('/logout')
def logout():
    logout(current_user)
    return redirect(url_for("principal_page"))
    
    return redirect(url_for('principal_page'))
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
from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory, send_file
from modulos import eckeys, users, fernet, rsa, restore, user2
from flask_login import login_user,login_required,UserMixin,LoginManager,current_user
from os import urandom, path

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
        user = request.form["usuario"]
        passw = request.form["password"]
        users.create_db()

        if users.login(user, passw):
            session['usuario'] = user

        return render_template('Form.html')
    else:
        return render_template('Form.html')
    
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
            #fernet.fernet_key_generator(user)
            eckeys.keys_generator(name, user, passwd, email)
            #rsa.rsa_key_generator(user, passwd)
            print(current_user)
            return redirect(url_for("uploads",nombre=user))
        return render_template("registro.html")
    return render_template("registro.html")
@app.route('/logout')
def logout():
    if 'usuario' in session:
        session.pop('usuario')
    
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
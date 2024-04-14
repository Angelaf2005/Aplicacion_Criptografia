from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory, send_file
from modulos import eckeys, users, fernet, rsa, restore, user2
from flask_login import login_user,login_required,UserMixin,LoginManager
from os import urandom, path

#app
app = Flask(__name__)
UPLOAD_FOLDER = "/Uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_manager_app = LoginManager(app)
# Generar clave de sesion
app.secret_key = urandom(32)
@login_manager_app.user_loader
def load_user(id):
    return user2.ModelUser.get_by_id(id)
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
        login_user(userconection)
    #fernet.fernet_key_generator(user)
    #eckeys.keys_generator(user,passw)
    #rsa.rsa_key_generator(user, passw)
    return render_template("registro.html")
@app.route('/logout')
def logout():
    if 'usuario' in session:
        session.pop('usuario')
    
    return redirect(url_for('principal_page'))
@app.route('/uploads/<name>')
@login_required
def download_file(name=""):
    basepath = path.dirname(__file__)
    url_file1 = path.join(basepath,"Private-Keys","foto.txt")
    respuesta = send_file(url_file1,as_attachment=True)
    print("hola")
    return respuesta


if __name__ == "__main__":
    app.run() # host='0.0.0.0'
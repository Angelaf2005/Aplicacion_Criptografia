from flask import Flask, render_template, request, session, redirect, url_for
from modulos import eckeys, users, fernet, rsa, restore
from os import urandom

app = Flask(__name__)

# Generar clave de sesion
app.secret_key = urandom(32)

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
        users.register(name,user,email,passwd)
    #fernet.fernet_key_generator(user)
    #eckeys.keys_generator(user,passw)
    #rsa.rsa_key_generator(user, passw)
    return render_template("registro.html")

@app.route('/logout')
def logout():
    if 'usuario' in session:
        session.pop('usuario')
    
    return redirect(url_for('principal_page'))


if __name__ == "__main__":
    app.run() # host='0.0.0.0'
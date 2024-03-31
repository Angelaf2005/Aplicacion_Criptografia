from flask import Flask, render_template, request
from modulos import eckeys
from modulos import users
from modulos import fernet

app = Flask(__name__)

@app.route("/")
def principal_page():
    return render_template("index.html")
@app.route("/login",  methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = request.form["usuario"]
        passw = request.form["password"]
        users.create_db()
        users.login(user, passw)
        return render_template('Form.html')
    else:
        return render_template('Form.html')
@app.route("/integrantes")
def integrantes():
    return render_template("integrantes.html")
@app.route("/registro")
def registro():
    #fernet.fernet_key_generator(user)
    #eckeys.keys_generator(passw,user)
    return render_template("registro.html")
if __name__ == "__main__":
    app.run()
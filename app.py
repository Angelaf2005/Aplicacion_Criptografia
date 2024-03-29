from flask import Flask, render_template, request
from modulos import eckeys

app = Flask(__name__)

@app.route("/")
def principal_page():
    return render_template("index.html")
@app.route("/login",  methods=["GET","POST"])
def login():
    if request.method == "POST":
        print(request.form["usuario"])
        print(request.form["password"])
        return render_template('Form.html')
    else:
        return render_template('Form.html')
@app.route("/integrantes")
def integrantes():
    return render_template("integrantes.html")
@app.route("/registro")
def registro():
    return render_template("registro.html")
if __name__ == "__main__":
    app.run()
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def principal_page():
    return render_template("index.html")
@app.route("/login")
def login():
    return render_template('Form.html')
if __name__ == "__main__":
    app.run()
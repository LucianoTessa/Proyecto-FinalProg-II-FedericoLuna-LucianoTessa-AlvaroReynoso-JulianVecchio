from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/publicar")
def publicar():
    return render_template("publicar.html")


@app.route("/favoritos")
def favoritos():
    return render_template("favoritos.html")


@app.route("/buscar")
def buscar():
    return render_template("buscar.html")


@app.route("/iniciar-sesion")
def login():
    return render_template("iniciar-sesion.html")


@app.route("/registrarse")
def registrarse():
    return render_template("registrarse.html")


if __name__ == "__main__":
    app.run(debug=True)

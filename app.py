import datetime
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:lomas0099@localhost/realstate"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(100))
    descripcion = db.Column(db.String(255))
    precio = db.Column(db.Float)
    tipo = db.Column(db.String(50))
    modalidad = db.Column(db.String(50))
    banios = db.Column(db.Integer)
    habitaciones = db.Column(db.Integer)
    metros_cuadrados = db.Column(db.Integer)
    ciudad = db.Column(db.String(50))
    # TODO: Agregar campo de imagen
    direccion = db.Column(db.String(255))
    fecha_publicacion = db.Column(db.DateTime)

    def __init__(
        self,
        titulo,
        descripcion,
        precio,
        tipo,
        modalidad,
        banios,
        habitaciones,
        metros_cuadrados,
        ciudad,
        direccion,
        fecha_publicacion,
    ):
        self.titulo = titulo
        self.descripcion = descripcion
        self.precio = precio
        self.tipo = tipo
        self.modalidad = modalidad
        self.banios = banios
        self.habitaciones = habitaciones
        self.metros_cuadrados = metros_cuadrados
        self.ciudad = ciudad
        self.direccion = direccion
        self.fecha_publicacion = fecha_publicacion



@app.route("/publicar", methods=["GET", "POST"])
def publicar():
    if request.method == "POST":
        titulo = request.form["titulo"]
        descripcion = request.form["descripcion"]
        precio = request.form["precio"]
        tipo = request.form["tipo"]
        modalidad = request.form["modalidad"]
        banios = request.form["banios"]
        habitaciones = request.form["habitaciones"]
        metros_cuadrados = request.form["metros_cuadrados"]
        ciudad = request.form["ciudad"]
        direccion = request.form["direccion"]

        nuevoPost = Post(
            titulo=titulo,
            descripcion=descripcion,
            precio=float(precio),
            tipo=tipo,
            modalidad=modalidad,
            banios=int(banios),
            habitaciones=int(habitaciones),
            metros_cuadrados=int(metros_cuadrados),
            ciudad=ciudad,
            direccion=direccion,
            fecha_publicacion=datetime.datetime.now(),
        )
        db.session.add(nuevoPost)
        db.session.commit()

    #HECHO EL MENSAJE DE EXITO Y REDIRECCIONAMIENTO EN 3 SEG A PAGINA PRINCIPAL
        flash("Publicación exitosa", "success")
        return render_template("publicar.html", delay=True)  # Enviar un indicador para hacer la espera

    return render_template("publicar.html")


app.secret_key = "tu_clave_secreta"

@app.route("/favoritos")
def favoritos():
    return render_template("favoritos.html")


@app.route("/buscar")
def buscar():
    # TODO: Obtener los posts de la base de datos
    postList = Post.query.all()
    return render_template("buscar.html", posts=postList)


@app.route("/iniciar-sesion")
def login():
    return render_template("iniciar-sesion.html")


@app.route("/registrarse")
def registrarse():
    return render_template("registrarse.html")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

import os
import datetime
from flask import Flask, render_template, request, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from werkzeug.utils import secure_filename
from dotenv import load_dotenv


load_dotenv()  # Cargar las variables de entorno desde el archivo .env


app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:lomas0099@localhost/realstate" // BD BOCHA

user = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PASSWORD")
host = os.getenv("DATABASE_HOST")
db_name = os.getenv("DATABASE_NAME")
app.secret_key = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{user}:{password}@{host}/{db_name}"
)
app.config["UPLOAD_FOLDER"] = "static/posts"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB
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
    imagen = db.Column(db.String(255))
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
        imagen,
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
        self.imagen = imagen
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
        metros_cuadrados = request.form["metros_cuadrados"]
        habitaciones = request.form["habitaciones"]
        imagen = request.files["imagen"]
        direccion = request.form["direccion"]
        ciudad = request.form["ciudad"]

        if imagen and imagen.filename != "":
            filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            nuevoPost = Post(
                titulo=titulo,
                descripcion=descripcion,
                precio=precio,
                tipo=tipo,
                modalidad=modalidad,
                banios=banios,
                habitaciones=habitaciones,
                metros_cuadrados=metros_cuadrados,
                ciudad=ciudad,
                direccion=direccion,
                fecha_publicacion=datetime.datetime.now(),
                imagen=filename,
            )
            db.session.add(nuevoPost)
            db.session.commit()
            flash("Publicación exitosa", "success")
        return render_template(
            "publicar.html", delay=True
        )  # Enviar un indicador para hacer la espera

    return render_template("publicar.html")


@app.route("/favoritos")
def favoritos():
    favoritosLista = Post.query.all()  # Aquí debes filtrar las publicaciones favoritas según tu lógica
    return render_template("favoritos.html",posts=favoritosLista)

@app.route("/eliminar_favorito/<int:id>", methods=["POST"])
def eliminar_favorito(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("favoritos"))


@app.route("/buscar")
def buscar():
    postList = Post.query.all()
    return render_template("buscar.html", posts=postList)


# TODO: Crear las rutas de detalle de cada post. Con metodo delete y get

@app.route("/post/<int:id>")
def post_detail(id):
    post = Post.query.get_or_404(id)
    return render_template("post_detail.html", post=post)

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

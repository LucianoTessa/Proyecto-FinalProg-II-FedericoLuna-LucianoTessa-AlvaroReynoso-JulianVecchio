import os
import datetime
from flask import Flask, render_template, request, flash, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()  # Cargar las variables de entorno desde el archivo .env

app = Flask(__name__)

user = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PASSWORD")
host = os.getenv("DATABASE_HOST")
db_name = os.getenv("DATABASE_NAME")
app.secret_key = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{user}:{password}@{host}/{db_name}"
)

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{user}:{password}@{host}/{db_name}"
app.config["UPLOAD_FOLDER"] = "static/posts"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
ma = Marshmallow(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    
    def __init__(self, username, email, password, apellido):
        self.username = username
        self.email = email
        self.password = password
        self.apellido = apellido

class MensajeForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)

    def __init__(self, nombre, email, mensaje):
        self.nombre = nombre
        self.email = email
        self.mensaje = mensaje
    

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
    esFavorito = db.Column(db.Boolean, default=False)

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
        esFavorito,
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
        self.esFavorito = esFavorito
        
# Crear la base de datos y las tablas
with app.app_context():
    db.create_all()

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
                esFavorito=False,
            )
            db.session.add(nuevoPost)
            db.session.commit()
            flash("Publicación exitosa", "success")
        return render_template(
            "publicar.html", delay=True
        )  # Enviar un indicador para hacer la espera

    return render_template("publicar.html")

@app.route("/enviar_mensaje", methods=["POST"])
def enviar_mensaje():
    nombre = request.form["nombre"]
    email = request.form["email"]
    mensaje = request.form["mensaje"]

    nuevo_mensaje = MensajeForm(nombre=nombre, email=email, mensaje=mensaje)
    db.session.add(nuevo_mensaje)
    db.session.commit()

    flash("Mensaje enviado exitosamente", "success")
    return redirect(url_for("index"))

@app.route("/favoritos")
def favoritos():
    favoritos = Post.query.filter_by(
        esFavorito=True
    ).all()  # Filtrar solo los posts favoritos
    return render_template("favoritos.html", posts=favoritos)

@app.route("/toggle_favorite/<int:post_id>", methods=["POST"])
def toggle_favorite(post_id):
    post = Post.query.get_or_404(post_id)
    post.esFavorito = not post.esFavorito  # Alternar el estado de esFavorito
    db.session.commit()
    return '', 204  # Responder con un estado 204 No Content

@app.route("/buscar")
def buscar():
    postList = Post.query.all()
    return render_template("buscar.html", posts=postList)

# TODO: Crear las rutas de detalle de cada post. Con metodo delete y get

@app.route("/post/<int:id>", methods=["GET", "DELETE"])
def post_detail(id):
    if request.method == "DELETE":
        post = Post.query.get_or_404(id)
        db.session.delete(post)
        db.session.commit()
        return render_template("buscar.html")
    elif request.method == "GET":
        post = Post.query.get_or_404(id)
        return render_template("post.html", post=post)

@app.route("/iniciar-sesion", methods=["GET", "POST"])
def iniciar_sesion():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            session["user_id"] = user.id
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for("index", welcome_message=f"Bienvenido, {user.username}!"))
        else:
            flash("Usuario o contraseña incorrecta", "danger")
    
    return render_template("iniciar_sesion.html")

@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        username = request.form["username"]
        apellido = request.form["apellido"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Las contraseñas no coinciden", "danger")
            return redirect(url_for("registrar"))

        # Verificar si el nombre de usuario o el correo electrónico ya existen
        user = User.query.filter((User.username == username) | (User.email == email)).first()
        if user:
            flash("El nombre de usuario o el correo electrónico ya están en uso", "danger")
            return redirect(url_for("registrar"))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        new_user = User(username=username, apellido=apellido, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash("Usuario registrado correctamente", "success")
        return redirect(url_for("index", welcome_message=f"Usuario registrado exitosamente, {username}!"))
    
    return render_template("registrarse.html")

@app.route("/")
def index():
    welcome_message = request.args.get("welcome_message")
    posts = Post.query.all()
    return render_template("index.html", welcome_message=welcome_message, posts=posts)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
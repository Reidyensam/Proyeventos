import requests
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://reidy@localhost/proyeventos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'tu_clave_secreta'

db = SQLAlchemy(app)

class Evento(db.Model):
    __tablename__ = 'eventos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(120), nullable=False)

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('inicio.html')

    @app.route('/contacto')
    def contacto():
        return render_template('contacto.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            response = requests.post('http://localhost:5001/usuarios/login', json={'username': username, 'password': password})
            if response.status_code == 200:
                session['username'] = username
                flash('¡Inicio de sesión exitoso!', 'success')
                return redirect(url_for('crear_evento'))
            else:
                flash('Nombre de usuario o contraseña incorrectos', 'danger')
        return render_template('login.html')

    @app.route('/registro', methods=['GET', 'POST'])
    def registro():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            response = requests.post('http://localhost:5001/usuarios', json={'username': username, 'email': email, 'password': password})
            if response.status_code == 201:
                flash('¡Registro exitoso!', 'success')
                return redirect(url_for('crear_evento'))
            else:
                flash('Error al registrar el usuario', 'danger')
        return render_template('registro.html')

    @app.route('/crear_evento', methods=['GET', 'POST'])
    def crear_evento():
        if request.method == 'POST':
            name = request.form['name']
            date = request.form['date']
            location = request.form['location']

            nuevo_evento = Evento(name=name, date=date, location=location)
            db.session.add(nuevo_evento)
            db.session.commit()

            flash('¡Evento creado exitosamente!', 'success')
            return redirect(url_for('lista_eventos'))
        return render_template('crear_evento.html')

    @app.route('/lista_eventos')
    def lista_eventos():
        eventos = Evento.query.all()
        return render_template('lista_eventos.html', eventos=eventos)

    @app.route('/enviar_notificacion', methods=['GET', 'POST'])
    def enviar_notificacion():
        if request.method == 'POST':
            recipients = request.form['recipients'].split(',')
            message = request.form['message']
            data = {'recipients': recipients, 'message': message}
            response = requests.post('http://localhost:5003/notificaciones', json=data)
            if response.status_code == 201:
                flash('¡Notificación enviada con éxito!', 'success')
            else:
                flash('Error al enviar la notificación', 'danger')
            return redirect(url_for('enviar_notificacion'))
        return render_template('notificaciones.html')

    @app.route('/notificacion_evento', methods=['POST'])
    def notificacion_evento():
        name = request.form['name']
        date = request.form['date']
        location = request.form['location']
        return render_template('notificaciones.html', name=name, date=date, location=location)

init_routes(app)

if __name__ == "__main__":
    app.app_context().push()  # Necesario para que la aplicación tenga el contexto de la base de datos
    db.create_all()  # Crea las tablas en la base de datos
    app.run(host='0.0.0.0', port=5000)

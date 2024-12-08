from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://reidy@localhost/proyeventos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'tu_clave_secreta'

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

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

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/registro', methods=['GET', 'POST'])
    def registro():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            # Crear nuevo usuario
            nuevo_usuario = Usuario(username=username, email=email, password=password)
            db.session.add(nuevo_usuario)
            db.session.commit()

            flash('¡Registro exitoso!', 'success')
            return redirect(url_for('crear_evento'))
        return render_template('registro.html')

    @app.route('/crear_evento', methods=['GET', 'POST'])
    def crear_evento():
        if request.method == 'POST':
            name = request.form['name']
            date = request.form['date']
            location = request.form['location']

            # Lógica para crear el evento (añadir a la base de datos)
            nuevo_evento = Evento(name=name, date=date, location=location)
            db.session.add(nuevo_evento)
            db.session.commit()

            flash('¡Evento creado exitosamente!', 'success')
            return redirect(url_for('index'))
        return render_template('crear_evento.html')

    @app.route('/usuarios', methods=['POST'])
    def create_user():
        data = request.form.to_dict()
        response = requests.post('http://localhost:5001/usuarios', json=data)
        if response.status_code == 201:
            return redirect('/crear_evento')
        else:
            return 'Error: Usuario no creado', response.status_code

init_routes(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

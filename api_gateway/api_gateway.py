from flask import Flask, render_template, redirect, request
import requests

app = Flask(__name__)

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

    @app.route('/registro')
    def registro():
        return render_template('registro.html')

    @app.route('/crear_evento')
    def crear_evento():
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

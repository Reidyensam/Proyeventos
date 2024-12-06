from flask import render_template, jsonify

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('inicio.html')

    @app.route('/contacto')
    def contacto():
        return render_template('contacto.html')

    @app.route('/registro')
    def registro():
        return render_template('registro.html')
    
    @app.route('/login')
    def login():
        return render_template('login.html')
    
    @app.route('/crear_evento')
    def crear_evento():
        return render_template('crear_evento.html')
    
    # Otras rutas pueden ser agregadas aquí...

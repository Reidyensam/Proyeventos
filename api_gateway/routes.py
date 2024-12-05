from flask import render_template, jsonify

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('inicio.html')

    @app.route('/registro')
    def registro():
        return render_template('registro.html')
    
    # Otras rutas pueden ser agregadas aquí...

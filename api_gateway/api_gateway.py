import sys
import os
from flask import Flask
from routes import init_routes

# Agregar la ruta raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configurar Flask para usar la carpeta de plantillas y estáticos correcta
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object('config.Config')

# Inicializar las rutas
init_routes(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

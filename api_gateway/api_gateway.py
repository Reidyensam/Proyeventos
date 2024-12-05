import sys
import os
from flask import Flask
from routes import init_routes

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)
app.config.from_object('config.Config')

init_routes(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

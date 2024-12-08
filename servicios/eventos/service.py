import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from flask import Flask, request, jsonify
from models import db, eventos  # Asegúrate de importar 'eventos' correctamente
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://reidy@localhost/proyeventos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/eventos', methods=['POST'])
def create_event():
    data = request.get_json()
    name = data['name']
    date = data['date']
    location = data['location']

    nuevo_evento = eventos(name=name, date=date, location=location)
    db.session.add(nuevo_evento)
    db.session.commit()

    return jsonify({'message': 'Evento creado correctamente'}), 201

@app.route('/eventos', methods=['GET'])
def get_events():
    eventos_list = eventos.query.all()
    eventos_data = [{"id": e.id, "name": e.name, "date": e.date, "location": e.location} for e in eventos_list]
    return jsonify(eventos_data)

if __name__ == "__main__":
    app.app_context().push()  # Necesario para que la aplicación tenga el contexto de la base de datos
    db.create_all()  # Crea las tablas en la base de datos
    app.run(host='0.0.0.0', port=5002)

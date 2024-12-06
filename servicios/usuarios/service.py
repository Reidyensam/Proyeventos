import sys
import os
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from flask import Flask, request, jsonify
from models import db, usuarios  # Importar correctamente la clase usuarios

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

logging.basicConfig(level=logging.DEBUG)

@app.route('/usuarios', methods=['POST'])
def create_user():
    app.logger.debug('Received POST request at /usuarios')
    data = request.get_json()
    app.logger.debug(f'Received data: {data}')
    new_user = usuarios(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    app.logger.debug('New user created and committed to database')
    return jsonify({'message': 'User created'}), 201

@app.route('/usuarios/login', methods=['POST'])
def login():
    app.logger.debug('Received POST request at /usuarios/login')
    data = request.get_json()
    app.logger.debug(f'Received data: {data}')
    user = usuarios.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        return jsonify({'message': 'Login successful'})
    return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == "__main__":
    app.run(port=5001)

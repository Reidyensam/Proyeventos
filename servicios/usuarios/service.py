from flask import Flask, request, jsonify
from models import db, User

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

@app.route('/usuarios', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201

@app.route('/usuarios/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        return jsonify({'message': 'Login successful'})
    return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == "__main__":
    app.run(port=5001)

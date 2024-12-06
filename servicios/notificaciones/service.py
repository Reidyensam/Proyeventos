import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from flask import Flask, request, jsonify
from models import db, Notification

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

@app.route('/notificaciones', methods=['POST'])
def send_notification():
    data = request.get_json()
    new_notification = Notification(message=data['message'], recipient=data['recipient'])
    db.session.add(new_notification)
    db.session.commit()
    return jsonify({'message': 'Notification sent'}), 201

if __name__ == "__main__":
    app.run(port=5003)

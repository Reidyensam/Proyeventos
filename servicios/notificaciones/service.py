import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from flask import Flask, request, jsonify
from models import db, notificaciones  # Asegúrate de que esto sea 'notificaciones' y no 'Notification'

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

@app.route('/notificaciones', methods=['POST'])
def send_notification():
    data = request.get_json()
    recipients = data['recipients']
    message = data['message']
    notifications = [notificaciones(message=message, recipient=recipient.strip()) for recipient in recipients]
    db.session.add_all(notifications)
    db.session.commit()
    return jsonify({'message': 'Notificaciones enviadas'}), 201

if __name__ == "__main__":
    app.run(port=5003)

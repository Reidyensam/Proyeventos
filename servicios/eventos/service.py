from flask import Flask, request, jsonify
from models import db, Event

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

@app.route('/eventos', methods=['POST'])
def create_event():
    data = request.get_json()
    new_event = Event(name=data['name'], date=data['date'], location=data['location'])
    db.session.add(new_event)
    db.session.commit()
    return jsonify({'message': 'Event created'}), 201

@app.route('/eventos', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([{'name': event.name, 'date': event.date, 'location': event.location} for event in events])

if __name__ == "__main__":
    app.run(port=5002)

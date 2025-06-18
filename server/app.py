from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Chatterbox API is running!</h1><p>Use /messages to interact with messages.</p>'

# ✅ GET /messages - list all messages ordered by created_at
@app.route('/messages', methods=['GET'])
def messages():
    messages = Message.query.order_by(Message.created_at).all()
    return jsonify([msg.to_dict() for msg in messages]), 200

# ✅ POST /messages - create new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    message = Message(
        body=data.get('body'),
        username=data.get('username')
    )
    db.session.add(message)
    db.session.commit()
    return jsonify(message.to_dict()), 201

@app.route("/messages/<int:id>")
def get_message(id):    
    messages = Message.query.filter_by(id=id).first()
    if messages: 
        # return jsonify([message.to_dict() for message in messages], 200)
        response = make_response(jsonify(messages.to_dict()), 200)

        return response
    
    else:
        return jsonify({"error": "Message not found"}, 404)

# ✅ PATCH /messages/<id> - update message body
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.get_json()
    if 'body' in data:
        message.body = data['body']
        message.updated_at = datetime.utcnow()  # manually update timestamp
        db.session.commit()
    return jsonify(message.to_dict()), 200

# ✅ DELETE /messages/<id> - delete message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(port=5555)






# from flask import Flask, request, make_response, jsonify
# from flask_cors import CORS
# from flask_migrate import Migrate

# from models import db, Message

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.json.compact = False

# CORS(app)
# migrate = Migrate(app, db)

# db.init_app(app)

# @app.route('/messages')
# def messages():
#     return ''

# @app.route('/messages/<int:id>')
# def messages_by_id(id):
#     return ''

# if __name__ == '__main__':
#     app.run(port=5555)

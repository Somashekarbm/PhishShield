from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from config import Config
from models import db, User

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
auth = HTTPTokenAuth(scheme='Bearer')
jwt = JWTManager(app)

# Dummy predictions (replace with actual ML model predictions later)
dummy_predictions = {
    "0": {"class": "benign", "probabilities": {"benign": 0.8, "phishing": 0.1, "malicious": 0.05, "defacement": 0.05}},
    "1": {"class": "phishing", "probabilities": {"benign": 0.1, "phishing": 0.7, "malicious": 0.1, "defacement": 0.1}},
    "2": {"class": "malicious", "probabilities": {"benign": 0.05, "phishing": 0.2, "malicious": 0.6, "defacement": 0.15}},
    "3": {"class": "defacement", "probabilities": {"benign": 0.1, "phishing": 0.1, "malicious": 0.2, "defacement": 0.6}}
}


def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"status": "error", "message": "User already exists"}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"status": "success", "userId": new_user.id}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"status": "success", "token": access_token}), 200
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401

@app.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({"status": "success"}), 200

@app.route('/api/admin/users', methods=['GET'])
@jwt_required()
def list_users():
    current_user = get_jwt_identity()
    # Assuming user with id 1 is the admin
    if current_user != 1:
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    users = User.query.all()
    user_list = [{"userId": user.id, "username": user.username, "email": user.email} for user in users]
    return jsonify({"users": user_list}), 200

@app.route('/api/admin/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user = get_jwt_identity()
    # Assuming user with id 1 is the admin
    if current_user != 1:
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return jsonify({"status": "success", "message": "User deleted"}), 200

@app.route('/api/user/data-deletion', methods=['POST'])
@jwt_required()
def request_data_deletion():
    current_user = get_jwt_identity()
    user = User.query.get_or_404(current_user)
    db.session.delete(user)
    db.session.commit()

    return jsonify({"status": "success", "message": "Data deletion requested"}), 200

@app.route('/api/classify', methods=['POST'])
def classify_url():
    data = request.get_json()
    url = data.get('url')
    model_id = data.get('model_id')

    # Validate input (ensure URL and model_id are present)
    if not url or model_id not in dummy_predictions:
        return jsonify({"error": "Invalid request data"}), 400

    # Dummy prediction (replace with actual ML model prediction logic)
    prediction = dummy_predictions[model_id]

    return jsonify({
        "class": prediction["class"],
        "probabilities": prediction["probabilities"]
    }), 200

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

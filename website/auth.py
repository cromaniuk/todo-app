from flask import Blueprint, request, jsonify
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token

auth = Blueprint('auth', __name__)

@auth.post('/register')
def register_user():
    if 'username' not in request.json:
        return jsonify({"error": "Missing username value"}), 403
  
    if 'password' not in request.json:
        return jsonify({"error": "Missing password value"}), 403
    
    username = request.json['username']
    password = request.json['password']

    user_exists = User.query.filter_by(username=username).first()
    if user_exists: 
        return jsonify({"error": "User already exists"}), 409
    
    if username and password:
        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created"}), 201
    
    return jsonify({"error": "422 Unprocessable Entity"}), 422


@auth.post('/login')
def login_user():
    if 'username' not in request.json:
        return jsonify({"error": "Missing username value"}), 403
  
    if 'password' not in request.json:
        return jsonify({"error": "Missing password value"}), 403
    
    username = request.json['username']
    password = request.json['password']

    user = User.query.filter_by(username=username).first()

    if username == user.username and check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        return jsonify({
            "message":"Logged in successfully",
            "tokens": {
                "access":access_token,
                "refresh":refresh_token
            }
        }), 200

    return jsonify({"error": "Invalid username or password"}), 400
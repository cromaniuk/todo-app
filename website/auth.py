from flask import Blueprint, request, jsonify
from . import db
from .models import User
from .schemas import UserSchema
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from marshmallow import ValidationError

auth = Blueprint("auth", __name__)


@auth.post("/register")
def register_user():
    schema = UserSchema()
    try:
        schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    username = request.json["username"]
    password = request.json["password"]

    user_exists = User.query.filter_by(username=username).first()
    if user_exists:
        return (
            jsonify({"error": "User already exists"}),
            409,
            {"Content-Type": "application/json"},
        )

    if username and password:
        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        return (
            jsonify({"message": "User created"}),
            201,
            {"Content-Type": "application/json"},
        )

    return (
        jsonify({"error": "422 Unprocessable Entity"}),
        422,
        {"Content-Type": "application/json"},
    )


@auth.post("/login")
def login_user():
    schema = UserSchema()
    try:
        result = schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    username = result["username"]
    password = result["password"]

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        return (
            jsonify(
                {
                    "message": "Logged in successfully",
                    "tokens": {"access": access_token, "refresh": refresh_token},
                }
            ),
            200,
        )

    return (
        jsonify({"error": "Invalid username or password"}),
        400,
        {"Content-Type": "application/json"},
    )

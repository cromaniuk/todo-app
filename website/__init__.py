from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

# Init app
def create_app(app_config=False):
    app = Flask(__name__)
    if app_config:
        app.config.update(app_config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
        app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.app_context().push()
    db.init_app(app)
    jwt.init_app(app)

    from .tasks import tasks
    from .auth import auth

    app.register_blueprint(tasks, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Task

    create_database(app)

    return app

def create_database(app):
    with app.app_context():
         db.create_all()
    print('Created database!')



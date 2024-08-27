import pytest
import json
from flask_jwt_extended import create_access_token

def test_successful_login(client, test_user):
        payload = json.dumps({
            "username": test_user.username,
            "password": test_user.password
        })
        response = client.post('/login', headers={"Content-Type": "application/json"}, data=payload)
        assert response.status_code == 200

def test_login_missing_username(client, test_user):
        payload = json.dumps({
            "password": test_user.password
        })
        response = client.post('/login', headers={"Content-Type": "application/json"}, data=payload)
        assert response.status_code == 403
        assert response.json['error']  == 'Missing username value'


def test_login_missing_password(client, test_user):
        payload = json.dumps({
            "username": test_user.username
        })
        response = client.post('/login', headers={"Content-Type": "application/json"}, data=payload)
        assert response.status_code == 403
        assert response.json['error']  == 'Missing password value'


def test_login_invalid_user(client, invalid_user):
        payload = json.dumps({
            "username": invalid_user.username,
            "password": invalid_user.password
        })
        response = client.post('/login', headers={"Content-Type": "application/json"}, data=payload)
        assert response.status_code == 400
        assert response.json['error']  == 'Invalid username or password'


def test_login_invalid_password(client, test_user):
        payload = json.dumps({
            "username": test_user.username,
            "password": "incorrectpassword"
        })
        response = client.post('/login', headers={"Content-Type": "application/json"}, data=payload)
        assert response.status_code == 400
        assert response.json['error']  == 'Invalid username or password'


def test_successful_registration(client, new_user):
        payload = json.dumps({
            "username": new_user.username,
            "password": new_user.password
        })
        response = client.post('/register', headers={"Content-Type": "application/json"}, data=payload)
        assert response.status_code == 201

def test_registration_user_already_exists(client, test_user):
        payload = json.dumps({
            "username": test_user.username,
            "password": test_user.password
        })
        response = client.post('/register', headers={"Content-Type": "application/json"}, data=payload)
        assert response.status_code == 409
        assert response.json['error']  == 'User already exists'

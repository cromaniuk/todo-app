import pytest
import json
from flask_jwt_extended import create_access_token

def test_get_task(client):
        response = client.get('/tasks/1', headers={"Content-Type": "application/json"})
        assert response.status_code == 200


def test_get_non_existant_task(client):
        response = client.get('/tasks/2', headers={"Content-Type": "application/json"})
        assert response.status_code == 404
        assert response.json['error']  == 'Task with ID 2 not found'


def test_get_tasks(client, test_user):
        access_token = create_access_token(test_user.username)
        headers = {
                "Authorization": "Bearer {}".format(access_token),
                "Content-Type": "application/json"
                }
        response = client.get('/tasks', headers=headers)
        assert response.status_code == 200


def test_get_tasks_no_auth(client):
        headers = {
                "Content-Type": "application/json"
                }
        response = client.get('/tasks', headers=headers)
        assert response.status_code == 401


def test_get_tasks_invalid_auth(client):
        headers = {
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNDcwMzAxMywianRpIjoiYmZhZThlNGYtNTc1NC00ZjU4LWE3YTctNTEyMjgxYzUxNWFjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InJvbWFuYzEiLCJuYmYiOjE3MjQ3MDMwMTMsImNzcmYiOiIyODE3Y2Y4NC0xNWFmLTRjOTEtYTNlMC04MGU0OWY1NjU2ZDIiLCJleHAiOjE3MjQ3MDM5MTN9.qC7-RjKNYG0lHHG7u1qb0AQmnVifRa9kdhYrIXLaJf4",
                "Content-Type": "application/json"
                }
        response = client.get('/tasks', headers=headers)
        assert response.status_code == 422


def test_add_task(client, new_task, test_user):
        access_token = create_access_token(test_user.username)
        payload = json.dumps({
            "title": new_task.title,
            "description": new_task.description,
            "completed": new_task.completed
        })
        headers = {
                "Authorization": "Bearer {}".format(access_token),
                "Content-Type": "application/json"
                }
        response = client.post('/tasks', headers=headers, data=payload)
        assert response.status_code == 201
        assert response.json['id'] == 2
        assert response.json['title'] == new_task.title
        assert response.json['description'] == new_task.description
        assert response.json['completed'] == new_task.completed


def test_add_task_no_auth(client, new_task):
        payload = json.dumps({
            "title": new_task.title,
            "description": new_task.description,
            "completed": new_task.completed,
        })
        headers = {
                "Content-Type": "application/json"
                }
        response = client.post('/tasks', headers=headers, data=payload)
        assert response.status_code == 401


def test_add_task_invalid_auth(client, new_task):
        payload = json.dumps({
            "title": new_task.title,
            "description": new_task.description,
            "completed": new_task.completed,
        })
        headers = {
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNDcwMzAxMywianRpIjoiYmZhZThlNGYtNTc1NC00ZjU4LWE3YTctNTEyMjgxYzUxNWFjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InJvbWFuYzEiLCJuYmYiOjE3MjQ3MDMwMTMsImNzcmYiOiIyODE3Y2Y4NC0xNWFmLTRjOTEtYTNlMC04MGU0OWY1NjU2ZDIiLCJleHAiOjE3MjQ3MDM5MTN9.qC7-RjKNYG0lHHG7u1qb0AQmnVifRa9kdhYrIXLaJf4",
                "Content-Type": "application/json"
                }
        response = client.post('/tasks', headers=headers, data=payload)
        assert response.status_code == 422


def test_update_task(client, updated_task, test_user):
        access_token = create_access_token(test_user.username)
        payload = json.dumps({
            "title": updated_task.title,
            "description": updated_task.description,
            "completed": updated_task.completed,
        })
        headers = {
                "Authorization": "Bearer {}".format(access_token),
                "Content-Type": "application/json"
                }
        response = client.put('/tasks/1', headers=headers, data=payload)
        assert response.status_code == 201
        assert response.json['id'] == 1
        assert response.json['title'] == updated_task.title
        assert response.json['description'] == updated_task.description
        assert response.json['completed'] == updated_task.completed


def test_update_task_invalid_auth(client, updated_task):
        payload = json.dumps({
            "title": updated_task.title,
            "description": updated_task.description,
            "completed": updated_task.completed
        })
        headers = {
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
                "Content-Type": "application/json"
                }
        response = client.put('/tasks/1', headers=headers, data=payload)
        assert response.status_code == 422

def test_update_non_existant_task(client, updated_task, test_user):
        access_token = create_access_token(test_user.username)
        payload = json.dumps({
            "title": updated_task.title,
            "description": updated_task.description,
            "completed": updated_task.completed,
        })
        headers = {
                "Authorization": "Bearer {}".format(access_token),
                "Content-Type": "application/json"
                }
        response = client.put('/tasks/2', headers=headers, data=payload)
        assert response.status_code == 404
        assert response.json['error']  == 'Task with ID 2 not found'


def test_delete_task(client, test_task, test_user):
        access_token = create_access_token(test_user.username)
        payload = json.dumps({
            "title": test_task.title,
            "description": test_task.description,
            "completed": test_task.completed,
        })
        headers = {
                "Authorization": "Bearer {}".format(access_token),
                "Content-Type": "application/json"
                }
        response = client.delete('/tasks/1', headers=headers, data=payload)
        assert response.status_code == 201


def test_delete_task_invalid_auth(client, test_task):
        payload = json.dumps({
            "title": test_task.title,
            "description": test_task.description,
            "completed": test_task.completed
        })
        headers = {
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
                "Content-Type": "application/json"
                }
        response = client.put('/tasks/1', headers=headers, data=payload)
        assert response.status_code == 422

def test_delete_non_existant_task(client, test_task, test_user):
        access_token = create_access_token(test_user.username)
        payload = json.dumps({
            "title": test_task.title,
            "description": test_task.description,
            "completed": test_task.completed,
        })
        headers = {
                "Authorization": "Bearer {}".format(access_token),
                "Content-Type": "application/json"
                }
        response = client.put('/tasks/2', headers=headers, data=payload)
        assert response.status_code == 404
        assert response.json['error']  == 'Task with ID 2 not found'


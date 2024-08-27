from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import db
from .models import Task
from .models import User
from .schemas import TaskSchema

tasks = Blueprint("tasks", __name__)


@tasks.post("/tasks")
@jwt_required()
def add_task():
    if "title" not in request.json:
        return jsonify({"error": "Missing title value"}), 403
    if "description" not in request.json:
        return jsonify({"error": "Missing description value"}), 403
    if "completed" not in request.json:
        return jsonify({"error": "Missing completed value"}), 403
    title = request.json["title"]
    description = request.json["description"]
    completed = request.json["completed"]
    user = User.query.filter_by(username=get_jwt_identity()).first()
    new_task = Task(
        title=title, description=description, completed=completed, user_id=user.id
    )
    db.session.add(new_task)
    db.session.commit()

    return TaskSchema().dumps(new_task), 201, {"Content-Type": "application/json"}


@tasks.get("/tasks")
@jwt_required()
def get_tasks():
    all_tasks = Task.query.all()
    return TaskSchema(many=True).dumps(all_tasks), {"Content-Type": "application/json"}


@tasks.put("/tasks/<int:task_id>")
@jwt_required()
def update_task(task_id):
    existing_task = db.session.get(Task, task_id)
    if existing_task:
        if "title" not in request.json:
            return (
                jsonify({"error": "Missing title value"}),
                403,
                {"Content-Type": "application/json"},
            )
        if "description" not in request.json:
            return (
                jsonify({"error": "Missing description value"}),
                403,
                {"Content-Type": "application/json"},
            )
        if "completed" not in request.json:
            return (
                jsonify({"error": "Missing completed value"}),
                403,
                {"Content-Type": "application/json"},
            )
        task = Task.query.filter_by(id=task_id).first()
        task.title = request.json["title"]
        task.description = request.json["description"]
        task.completed = request.json["completed"]
        db.session.add(task)
        db.session.commit()
        return TaskSchema().dumps(task), 201, {"Content-Type": "application/json"}
    else:
        return (
            jsonify({"error": f"Task with ID {task_id} not found"}),
            404,
            {"Content-Type": "application/json"},
        )


@tasks.delete("/tasks/<int:task_id>")
@jwt_required()
def delete_task(task_id):
    existing_task = db.session.get(Task, task_id)
    if existing_task:
        task = Task.query.filter_by(id=task_id).first()
        db.session.delete(task)
        db.session.commit()
        return (
            jsonify({"message": f"Task with ID {task_id} successfully deleted"}),
            201,
            {"Content-Type": "application/json"},
        )
    else:
        return (
            jsonify({"error": f"Task with ID {task_id} not found"}),
            404,
            {"Content-Type": "application/json"},
        )


@tasks.get("/tasks/<int:task_id>")
def get_task(task_id):
    existing_task = db.session.get(Task, task_id)
    if existing_task:
        task = Task.query.filter_by(id=task_id).first()
    else:
        return (
            jsonify({"error": f"Task with ID {task_id} not found"}),
            404,
            {"Content-Type": "application/json"},
        )
    return TaskSchema().dumps(task), 200, {"Content-Type": "application/json"}

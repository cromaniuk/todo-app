from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from .models import User, Task


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User

    id = auto_field()
    username = auto_field()


class TaskSchema(SQLAlchemySchema):
    class Meta:
        model = Task

    id = auto_field()
    title = auto_field()
    description = auto_field()
    completed = auto_field()

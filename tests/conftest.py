import pytest
from website import create_app, db
from website.models import Task, User
from werkzeug.security import generate_password_hash

@pytest.fixture(scope="session")
def app():
    test_config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db",
        "JWT_SECRET_KEY":"test_secret_key"
    }
    app = create_app(test_config)

    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def client(app):
   test_user = User(username="test_user_1", password=generate_password_hash("testing1"))
   test_task = Task(title="test title", description="test description", completed=True, user_id=test_user.id)
   db.session.add(test_user)
   db.session.add(test_task)
   db.session.commit()
   yield app.test_client()
   with app.app_context():
    clear_data(db.session)


def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        session.execute(table.delete())
    session.commit()


@pytest.fixture(scope="module")
def test_user():
    test_user = User(username="test_user_1", password="testing1")
    yield test_user


@pytest.fixture(scope="module")
def invalid_user():
    test_user = User(username="test_user_2", password="testing2")
    yield test_user


@pytest.fixture(scope="module")
def new_user():
    test_user = User(username="test_user_3", password="testing3")
    yield test_user


@pytest.fixture(scope="module")
def test_task():
    test_task = Task(title="test title", description="test description", completed=True)
    yield test_task


@pytest.fixture(scope="module")
def updated_task():
    test_task = Task(title="test title updated", description="test description updated", completed=False)
    yield test_task


@pytest.fixture(scope="module")
def new_task():
    test_task = Task(title="new test title", description="new test description", completed=False)
    yield test_task



# To Do App API

## Setup & Installation

Make sure you have the latest version of Python installed.

```bash
git clone <repo-url>
```

```bash
install pipenv
```

Rename .env.template to .env

Create a secret key and update the JWT_SECRET_KEY in .env to the created value

## Running The App

Activate shell to create virtual environment

```shell
pipenv shell
```

Run development server

```bash
Flask run
```

## Viewing The App

Go to `http://127.0.0.1:8000`

## Running Tests

Install dependencies

```bash
pipenv sync --dev
```

Run tests

```bash
pytest tests
```

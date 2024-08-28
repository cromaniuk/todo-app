# Run server
from website import create_app
import os
from werkzeug.exceptions import HTTPException
import json

app = create_app()

@app.errorhandler(HTTPException)
def handle_exception(e):
#Return JSON instead of HTML for HTTP errors
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

if __name__ == "__main__":
    app.run(
        debug=os.getenv("FLASK_DEBUG"),
        host=os.getenv("FLASK_RUN_HOST"),
        port=os.getenv("FLASK_RUN_PORT"),
    )

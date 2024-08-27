# Run server
from website import create_app
import os

app = create_app()

if __name__ == "__main__":
    app.run(
        debug=os.getenv("FLASK_DEBUG"),
        host=os.getenv("FLASK_RUN_HOST"),
        port=os.getenv("FLASK_RUN_PORT"),
    )

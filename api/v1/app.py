#!/usr/bin/python3
"""Create a new Flask app"""
from os import environ

from flask import Flask

from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Teardown appcontext"""
    storage.close()


if __name__ == "__main__":
    host = environ.get("HBNB_API_HOST")
    port = environ.get("HBNB_API_PORT")
    if not host:
        host = "0.0.0.0"

    if not port:
        port = "5000"
    app.run(host=host, port=port, threaded=True)

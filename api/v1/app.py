#!/usr/bin/python3
"""Creates a Flask app"""

from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

# Register app_views with Blueprint
app.register_blueprint(app_views)
app.url_map.strict_slashes = False

@app.teardown_appcontext
def teardown_app(exception):
    """Handles app tear down"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """Handle 404 Error - Resource not found"""
    response = {"error": "Not found"}
    return (jsonify(response), 404)


if __name__ == "__main__":
    # get host & port from environment variables.
    HOST = getenv("HBNB_API_HOST", "0.0.0.0")
    PORT = int(getenv("HBNB_API_PORT", "5000"))

    # Running app in multi thread to boost performance
    app.run(host=HOST, port=PORT, threaded=True)

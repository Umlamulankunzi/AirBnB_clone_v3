#!/usr/bin/python3
"""Creates a Flask app"""

from flask import Flask
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

#!/usr/bin/python3
"""Create Blueprint instance with 'url_prefix' set to '/api/v1'"""

from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/vi")


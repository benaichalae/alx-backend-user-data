#!/usr/bin/env python3
"""Module of Index views.
"""
from flask import jsonify, abort, Blueprint
from api.v1.views import app_views

# Define a new Blueprint for the index views
index_views = Blueprint('index_views', __name__)

@index_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """GET /api/v1/status
    Return:
      - the status of the API.
    """
    return jsonify({"status": "OK"})

@index_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """GET /api/v1/stats
    Return:
      - the number of each objects.
    """
    from models.user import User
    stats = {
        'users': User.count()
    }
    return jsonify(stats)

@index_views.route('/unauthorized/', strict_slashes=False)
def unauthorized() -> None:
    """GET /api/v1/unauthorized
    Return:
      - Unauthorized error.
    """
    abort(401)

@index_views.route('/forbidden/', strict_slashes=False)
def forbidden() -> None:
    """GET /api/v1/forbidden
    Return:
      - Forbidden error.
    """
    abort(403)

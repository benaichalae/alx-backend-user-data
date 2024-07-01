#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from api.v1.views import app_views

# Import specific authentication classes based on environment variable
auth = None
auth_type = getenv("AUTH_TYPE")

if auth_type == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif auth_type == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif auth_type == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
elif auth_type == "session_db_auth":
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()
else:
    from api.v1.auth.auth import Auth
    auth = Auth()

# Create Flask application
app = Flask(__name__)
app.register_blueprint(app_views)

# Enable CORS for all endpoints under /api/v1/*
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({"error": "Forbidden"}), 403

# Before request handler
@app.before_request
def before_request():
    """Filtering of each request"""
    if auth is None:
        return

    # Assign current_user to request object if authentication exists
    request.current_user = auth.current_user(request)

    # Define excluded paths from authentication check
    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/',
                      '/api/v1/auth_session/login/']

    # Perform authentication and authorization checks
    if (request.path not in excluded_paths and
        auth.require_auth(request.path, excluded_paths)):

        if (auth.authorization_header(request) is None and
            auth.session_cookie(request) is None):
            abort(401)

        if auth.current_user(request) is None:
            abort(403)

# Main application entry point
if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)

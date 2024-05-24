#!/usr/bin/env python3
"""Route module for the API.
"""
import os
from flask import Flask, jsonify, abort, request
from flask_cors import CORS

from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth

def create_app():
    """Create and configure the app."""
    app = Flask(__name__)
    app.register_blueprint(app_views)
    CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

    auth = initialize_auth()

    @app.errorhandler(404)
    def not_found(error) -> str:
        """Not found handler."""
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(401)
    def unauthorized(error) -> str:
        """Unauthorized handler."""
        return jsonify({"error": "Unauthorized"}), 401

    @app.errorhandler(403)
    def forbidden(error) -> str:
        """Forbidden handler."""
        return jsonify({"error": "Forbidden"}), 403

    @app.before_request
    def authenticate_user():
        """Authenticates a user before processing a request."""
        if auth:
            excluded_paths = [
                '/api/v1/status/',
                '/api/v1/unauthorized/',
                '/api/v1/forbidden/',
            ]
            if auth.require_auth(request.path, excluded_paths):
                auth_header = auth.authorization_header(request)
                user = auth.current_user(request)
                if auth_header is None:
                    abort(401)
                if user is None:
                    abort(403)

    return app

def initialize_auth():
    """Initialize the appropriate auth type based on environment variable."""
    auth_type = os.getenv('AUTH_TYPE', 'auth')
    if auth_type == 'basic_auth':
        return BasicAuth()
    return Auth()

if __name__ == "__main__":
    app = create_app()
    host = os.getenv("API_HOST", "0.0.0.0")
    port = os.getenv("API_PORT", "5000")
    app.run(host=host, port=port)
#!/usr/bin/env python3
"""
Handles all routes for session-based authentication.
"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Endpoint for user login and session creation.

    POST /api/v1/auth_session/login

    JSON body:
      - email: User's email address.
      - password: User's password.

    Returns:
      - JSON object representing the authenticated user.
      - 400 if email or password is missing.
      - 404 if no user is found for the given email.
      - 401 if the password is incorrect.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    found_user = User.search({'email': email})
    if not found_user:
        return jsonify({"error": "no user found for this email"}), 404

    user = found_user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    user_json = user.to_json()
    response = jsonify(user_json)
    session_name = getenv("SESSION_NAME")
    response.set_cookie(session_name, session_id)

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Endpoint for user logout.

    DELETE /api/v1/auth_session/logout

    Returns:
      - Empty JSON object upon successful logout.
      - 404 if unable to destroy the session.
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({})

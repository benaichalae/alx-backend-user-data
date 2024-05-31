#!/usr/bin/env python3
"""A simple Flask app with user authentication features.
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)
auth = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    """GET /
    Return:
        - The home page's payload.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """POST /users
    Return:
        - The account creation payload.
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        auth.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login_user():
    """POST /sessions
    Return:
        - The account login payload.
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not auth.valid_login(email, password):
        abort(401)
    session_id = auth.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout_user():
    """DELETE /sessions
    Return:
        - Redirects to home route.
    """
    session_id = request.cookies.get("session_id")
    user = auth.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    auth.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def user_profile():
    """GET /profile
    Return:
        - The user's profile information.
    """
    session_id = request.cookies.get("session_id")
    user = auth.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def request_reset_token():
    """POST /reset_password
    Return:
        - The user's password reset payload.
    """
    email = request.form.get("email")
    try:
        reset_token = auth.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def reset_user_password():
    """PUT /reset_password
    Return:
        - The user's password updated payload.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        auth.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

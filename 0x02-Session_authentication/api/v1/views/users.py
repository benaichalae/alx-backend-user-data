#!/usr/bin/env python3
"""
Module for Users views
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """GET /api/v1/users
    Returns:
        - List of all User objects JSON represented
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """GET /api/v1/users/:id
    Path parameter:
        - user_id (str): User ID to retrieve
    Returns:
        - JSON: User object representation
        - 404: If the specified User ID doesn't exist
    """
    if user_id is None:
        abort(404)

    if user_id == 'me':
        if not request.current_user:
            abort(404)
        return jsonify(request.current_user.to_json()), 200

    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """DELETE /api/v1/users/:id
    Path parameter:
        - user_id (str): User ID to delete
    Returns:
        - JSON: Empty response if the User has been correctly deleted
        - 404: If the specified User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """POST /api/v1/users/
    JSON body:
        - email (str): Email address of the new User
        - password (str): Password for the new User
        - last_name (optional): Last name of the new User
        - first_name (optional): First name of the new User
    Returns:
        - JSON: Newly created User object representation
        - 400: If there is an issue creating the new User
    """
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'email and password are required'}), 400

        user = User(email=email, password=password)
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.save()
        return jsonify(user.to_json()), 201

    except Exception as e:
        return jsonify({'error': f"Can't create User: {str(e)}"}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """PUT /api/v1/users/:id
    Path parameter:
        - user_id (str): User ID to update
    JSON body:
        - last_name (optional): New last name for the user
        - first_name (optional): New first name for the user
    Returns:
        - JSON: Updated User object representation
        - 404: If the specified User ID doesn't exist
        - 400: If there is an issue updating the User
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    
    try:
        data = request.get_json()

        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        
        user.save()
        return jsonify(user.to_json()), 200
    
    except Exception as e:
        return jsonify({'error': f"Can't update User: {str(e)}"}), 400


if __name__ == "__main__":
    pass  # Application run within a Flask environment, not executed directly

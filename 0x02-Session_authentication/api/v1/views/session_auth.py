#!/usr/bin/env python3
"""
    This module contains the routes for the Session authentication
"""
from api.v1.views import app_views
from flask import request, jsonify
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', strict_slashes=False, methods=['POST'])
def post_login():
    """ POST /auth_session/login
    - Return the dictionary representation of the User
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None:
        return jsonify({'error': 'email missing'}), 400
    if password is None:
        return jsonify({'error': 'password missing'}), 400
    email = {'email': email}
    user = User.search(attributes=email)
    if user is None or user == []:
        return jsonify({'error': 'no user found for this email'}), 404
    password_correct = user[0].is_valid_password(password)
    if not password_correct or password_correct is None:
        return jsonify({'error': 'wrong password'}), 401
    from api.v1.app import auth

    session_id = auth.create_session(user[0].id)
    session_name = getenv('SESSION_NAME')
    out = jsonify(user[0].to_json())
    out.set_cookie(session_name, session_id)
    return out

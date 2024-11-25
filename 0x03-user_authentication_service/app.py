#!/usr/bin/env python3
"""
    This module contains the setup for the Flask
"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth


AUTH = Auth()


app = Flask(__name__)


@app.route('/', strict_slashes=False, methods=['GET'])
def home_route():
    """ GET '/'
      - Returns a jsonified message
    """
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', strict_slashes=False, methods=['POST'])
def user():
    """ POST '/users'
      - Returns a newly created user
    """
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        user = AUTH.register_user(email, password)
        if user:
            return jsonify({'email': email, 'message': 'user created'})
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400


@app.route('/sessions', strict_slashes=False, methods=['POST'])
def login():
    """ POST '/sessions'
      - Return jsonify response message
    """
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)
            if session_id:
                out = jsonify({'email': email, 'message': 'logged in'})
                out.set_cookie('session_id', session_id)
                return out
        abort(401)
    except Exception:
        abort(401)


@app.route('/sessions', strict_slashes=True, methods=['DELETE'])
def logout():
    """ DELETE /sessions
      - Return
    """
    try:
        session_id = request.cookie.get('session_id')
        if session_id:
            user = AUTH.get_user_by_session_id(session_id)
            if user:
                AUTH.destroy_session(session_id)
                return redirect(url_for('home_route'))
        abort(403)
    except Exception:
        abort(403)


@app.route('/profile', strict_slashes=True, methods=['GET'])
def profile():
    """ GET /profile
      - Return a jsnonify message
    """
    try:
        session_id = request.cookie.get('session_id')
        if session_id:
            user = AUTH.get_user_by_session_id(session_id)
            if user:
                return jsonify({'email': email})
        abort(403)
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')

#!/usr/bin/env python3
"""
    This module contains the setup for the Flask
"""
from flask import Flask, jsonify, request, abort
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
    """ GET '/login'
      - Return
    """
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)
            if session_id:
                out = jsonify({'email': email, 'password': password})
                out.set_cookie('session_id', session_id)
                return out
        abort(401)
    except Exception:
        abort(401)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')

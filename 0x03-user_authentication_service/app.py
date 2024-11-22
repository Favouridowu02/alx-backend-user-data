#!/usr/bin/env python3
"""
    This module contains the setup for the Flask
"""
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')

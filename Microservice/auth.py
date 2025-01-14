from functools import wraps
from flask import request, jsonify, session
import jwt
import datetime

SECRET_KEY = "COMP2001Trails"

def authenticate_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'email' not in session:
            return jsonify({'message': 'User not logged in'}), 401
        request.user_info = {'email': session['email'], 'role': session['role']}
        return f(*args, **kwargs)
    return wrapper

def required_role(required_role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_info = getattr(request, 'user_info', None)
            if not user_info or user_info.get('role') != required_role:
                return jsonify({'message': 'Unauthorized, insufficient role'}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator

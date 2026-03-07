from functools import wraps
from flask import request, jsonify, g, current_app
from app.utils.helpers import decode_token
from app.models.user import User
from app.extensions import db
import jwt


def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')

        if not auth_header.startswith('Bearer '):
            current_app.logger.warning(f'jwt_required: missing/bad header → "{auth_header[:30]}"')
            return jsonify({'error': 'Missing or invalid authorization header'}), 401

        token = auth_header.split(' ', 1)[1]
        try:
            payload = decode_token(token)
        except jwt.ExpiredSignatureError:
            current_app.logger.warning('jwt_required: token expired')
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError as e:
            current_app.logger.warning(f'jwt_required: invalid token → {e}')
            return jsonify({'error': 'Invalid token'}), 401

        user = db.session.get(User, int(payload['sub']))
        if not user:
            current_app.logger.warning(f'jwt_required: user {payload["sub"]} not found')
            return jsonify({'error': 'User not found'}), 401
        if not user.is_active:
            current_app.logger.warning(f'jwt_required: user {user.email} inactive')
            return jsonify({'error': 'Account inactive'}), 401

        g.current_user = user
        return f(*args, **kwargs)
    return decorated


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get('Authorization', '')

            if not auth_header.startswith('Bearer '):
                current_app.logger.warning(f'role_required: missing/bad header for {f.__name__}')
                return jsonify({'error': 'Missing or invalid authorization header'}), 401

            token = auth_header.split(' ', 1)[1]
            try:
                payload = decode_token(token)
            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token expired'}), 401
            except jwt.InvalidTokenError as e:
                current_app.logger.warning(f'role_required: invalid token → {e}')
                return jsonify({'error': 'Invalid token'}), 401

            user = db.session.get(User, int(payload['sub']))
            if not user:
                current_app.logger.warning(f'role_required: user {payload["sub"]} not found')
                return jsonify({'error': 'User not found'}), 401
            if not user.is_active:
                return jsonify({'error': 'Account inactive'}), 401

            if user.role not in roles:
                current_app.logger.warning(f'role_required: role {user.role!r} not in {roles}')
                return jsonify({'error': 'Insufficient permissions'}), 403

            g.current_user = user
            return f(*args, **kwargs)
        return decorated
    return decorator

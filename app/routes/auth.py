from flask import Blueprint, request, jsonify, g
from app.extensions import db
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.utils.helpers import (
    verify_password, hash_password,
    generate_access_token, generate_refresh_token, decode_token,
    update_streak,
)
from app.utils.decorators import jwt_required
from datetime import datetime, timezone
import jwt as pyjwt

auth_bp = Blueprint('auth', __name__)


@auth_bp.post('/login')
def login():
    data = request.get_json(silent=True) or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not verify_password(password, user.password_hash):
        return jsonify({'error': 'Invalid email or password'}), 401

    if not user.is_active:
        return jsonify({'error': 'Account is inactive. Contact your administrator.'}), 403

    if user.college and not user.college.is_active:
        return jsonify({'error': 'Your college account has been deactivated. Contact the platform administrator.'}), 403

    access_token = generate_access_token(user.id, user.role)
    refresh_token_str, expires_at = generate_refresh_token(user.id)

    rt = RefreshToken(user_id=user.id, token=refresh_token_str, expires_at=expires_at)
    db.session.add(rt)

    # Update last_active and streak
    user.last_active = datetime.now(timezone.utc)
    update_streak(user.id)
    db.session.commit()

    return jsonify({
        'token': access_token,
        'refreshToken': refresh_token_str,
        'user': user.to_dict(),
    }), 200


@auth_bp.patch('/complete-onboarding')
@jwt_required
def complete_onboarding():
    user = g.current_user
    data = request.get_json(silent=True) or {}

    # Update profile fields (support both frontend field names and backend field names)
    name = data.get('full_name') or data.get('name', '')
    if name:
        user.name = name.strip()
    if 'phone' in data:
        user.phone = data['phone'].strip()
    linkedin = data.get('linkedin_url') or data.get('linkedin', '')
    if linkedin is not None:
        user.linkedin = linkedin.strip()
    if 'branch' in data:
        user.branch = data['branch'].strip()
    if 'section' in data:
        user.section = data['section'].strip()
    if 'roll_number' in data:
        user.roll_number = data['roll_number'].strip()
    if 'passout_year' in data:
        user.passout_year = int(data['passout_year'])

    # Set new password (frontend sends new_password)
    new_password = data.get('new_password') or data.get('password', '')
    if not new_password or len(new_password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400

    user.password_hash = hash_password(new_password)
    user.first_login = False

    db.session.commit()

    return jsonify({'message': 'Onboarding complete', 'user': user.to_dict()}), 200


@auth_bp.post('/refresh')
def refresh():
    data = request.get_json(silent=True) or {}
    token_str = data.get('refreshToken', '')

    if not token_str:
        return jsonify({'error': 'Refresh token required'}), 400

    try:
        payload = decode_token(token_str)
    except pyjwt.ExpiredSignatureError:
        return jsonify({'error': 'Refresh token expired'}), 401
    except pyjwt.InvalidTokenError:
        return jsonify({'error': 'Invalid refresh token'}), 401

    rt = RefreshToken.query.filter_by(token=token_str).first()
    if not rt or rt.is_expired():
        return jsonify({'error': 'Refresh token not found or expired'}), 401

    user = User.query.get(payload['sub'])
    if not user or not user.is_active:
        return jsonify({'error': 'User not found'}), 401

    # Rotate refresh token
    db.session.delete(rt)
    new_access = generate_access_token(user.id, user.role)
    new_refresh_str, expires_at = generate_refresh_token(user.id)
    new_rt = RefreshToken(user_id=user.id, token=new_refresh_str, expires_at=expires_at)
    db.session.add(new_rt)
    db.session.commit()

    return jsonify({'token': new_access, 'refreshToken': new_refresh_str}), 200


@auth_bp.post('/logout')
@jwt_required
def logout():
    data = request.get_json(silent=True) or {}
    refresh_token_str = data.get('refreshToken', '')
    if refresh_token_str:
        rt = RefreshToken.query.filter_by(token=refresh_token_str).first()
        if rt:
            db.session.delete(rt)
            db.session.commit()
    return jsonify({'message': 'Logged out'}), 200


@auth_bp.get('/activate')
def validate_activation_token():
    """Validate token only — used by frontend to check before showing set-password form."""
    token = request.args.get('token', '')
    if not token:
        return jsonify({'error': 'Token required'}), 400

    from app.models.college import College
    college = College.query.filter_by(activation_token=token).first()
    if not college:
        return jsonify({'error': 'Invalid or already used activation token'}), 404

    return jsonify({'message': 'Token valid', 'college': college.name}), 200


@auth_bp.post('/activate')
def activate():
    """Activate account and set password."""
    data = request.get_json(silent=True) or {}
    token = data.get('token', '')
    password = data.get('password', '')

    if not token:
        return jsonify({'error': 'Token required'}), 400
    if not password or len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400

    from app.models.college import College
    from app.utils.helpers import hash_password
    college = College.query.filter_by(activation_token=token).first()
    if not college:
        return jsonify({'error': 'Invalid or already used activation token'}), 404

    admin = User.query.filter_by(college_id=college.id, role='college_admin').first()
    if not admin:
        return jsonify({'error': 'Admin not found'}), 404

    college.activated_at = datetime.now(timezone.utc)
    college.activation_token = None
    college.is_active = True
    admin.is_active = True
    admin.password_hash = hash_password(password)
    admin.first_login = False
    db.session.commit()

    return jsonify({'message': 'Account activated. You can now log in.'}), 200

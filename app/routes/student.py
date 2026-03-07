from flask import Blueprint, request, jsonify, g
from app.extensions import db
from app.utils.decorators import role_required
from app.utils.helpers import hash_password, verify_password

student_bp = Blueprint('student', __name__)


@student_bp.get('/profile')
@role_required('student', 'college_admin', 'super_admin')
def get_profile():
    return jsonify(g.current_user.to_dict()), 200


@student_bp.patch('/profile')
@role_required('student', 'college_admin', 'super_admin')
def update_profile():
    user = g.current_user
    data = request.get_json(silent=True) or {}

    updatable = ['name', 'phone', 'linkedin', 'branch', 'section',
                 'roll_number', 'passout_year',
                 'email_notifications', 'assignment_reminders', 'leaderboard_updates']

    for field in updatable:
        if field in data:
            setattr(user, field, data[field])

    # Handle password change
    if 'current_password' in data and 'new_password' in data:
        if not verify_password(data['current_password'], user.password_hash):
            return jsonify({'error': 'Current password is incorrect'}), 400
        if len(data['new_password']) < 8:
            return jsonify({'error': 'New password must be at least 8 characters'}), 400
        user.password_hash = hash_password(data['new_password'])

    db.session.commit()
    return jsonify({'message': 'Profile updated', 'user': user.to_dict()}), 200

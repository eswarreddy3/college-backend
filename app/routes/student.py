from datetime import datetime, timezone, timedelta
from flask import Blueprint, request, jsonify, g
from app.extensions import db
from app.models.user import User
from app.models.activity_log import ActivityLog
from app.models.coding_problem import CodingSubmission
from app.models.streak import UserStreak
from app.utils.decorators import role_required, jwt_required
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

    if 'current_password' in data and 'new_password' in data:
        if not verify_password(data['current_password'], user.password_hash):
            return jsonify({'error': 'Current password is incorrect'}), 400
        if len(data['new_password']) < 8:
            return jsonify({'error': 'New password must be at least 8 characters'}), 400
        user.password_hash = hash_password(data['new_password'])

    db.session.commit()
    return jsonify({'message': 'Profile updated', 'user': user.to_dict()}), 200


@student_bp.get('/dashboard')
@role_required('student')
def dashboard():
    user = g.current_user

    # College rank by points
    rank = (
        User.query
        .filter_by(college_id=user.college_id, role='student')
        .filter(User.points > user.points)
        .count()
    ) + 1

    total_in_college = User.query.filter_by(college_id=user.college_id, role='student').count()

    # Solved problems count
    solved_count = (
        db.session.query(CodingSubmission.problem_id)
        .filter_by(user_id=user.id, status='accepted')
        .distinct()
        .count()
    )

    # Recent activity (last 10)
    recent_activity = (
        ActivityLog.query
        .filter_by(user_id=user.id)
        .order_by(ActivityLog.created_at.desc())
        .limit(10)
        .all()
    )

    # Streak from user_streaks table
    streak_row = UserStreak.query.filter_by(user_id=user.id).first()
    current_streak = streak_row.current_streak if streak_row else 0
    longest_streak = streak_row.longest_streak if streak_row else 0

    # Active days this month (for streak calendar)
    now = datetime.now(timezone.utc)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_logs = (
        ActivityLog.query
        .filter(ActivityLog.user_id == user.id, ActivityLog.created_at >= month_start)
        .all()
    )
    active_days = sorted(set(log.created_at.day for log in monthly_logs))

    return jsonify({
        'points': user.points,
        'streak': current_streak,
        'longest_streak': longest_streak,
        'rank': rank,
        'total_in_college': total_in_college,
        'solved_count': solved_count,
        'active_days': active_days,
        'recent_activity': [a.to_dict() for a in recent_activity],
    }), 200


@student_bp.get('/leaderboard')
@role_required('student')
def leaderboard():
    user = g.current_user
    scope = request.args.get('scope', 'college')  # college | branch | section

    query = User.query.filter_by(college_id=user.college_id, role='student')
    if scope == 'branch' and user.branch:
        query = query.filter_by(branch=user.branch)
    elif scope == 'section' and user.section:
        query = query.filter_by(branch=user.branch, section=user.section)

    students = query.order_by(User.points.desc()).all()

    result = []
    for i, s in enumerate(students):
        result.append({
            'rank': i + 1,
            'id': s.id,
            'name': s.name,
            'branch': s.branch,
            'section': s.section,
            'points': s.points,
            'streak': s.streak,
            'is_current_user': s.id == user.id,
        })

    return jsonify(result), 200

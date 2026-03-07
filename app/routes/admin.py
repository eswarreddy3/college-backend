from flask import Blueprint, request, jsonify, g
from app.extensions import db
from app.models.user import User
from app.utils.decorators import role_required
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__)


@admin_bp.get('/students')
@role_required('college_admin')
def get_students():
    college_id = g.current_user.college_id
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '').strip()

    query = User.query.filter_by(college_id=college_id, role='student')
    if search:
        query = query.filter(
            (User.name.ilike(f'%{search}%')) | (User.email.ilike(f'%{search}%'))
        )

    pagination = query.order_by(User.name).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'students': [u.to_dict() for u in pagination.items],
        'total': pagination.total,
        'page': page,
        'pages': pagination.pages,
    }), 200


@admin_bp.get('/analytics')
@role_required('college_admin')
def get_analytics():
    college_id = g.current_user.college_id

    total_students = User.query.filter_by(college_id=college_id, role='student').count()
    active_students = User.query.filter_by(college_id=college_id, role='student', is_active=True).count()
    onboarded = User.query.filter_by(college_id=college_id, role='student', first_login=False).count()

    # Top students by points
    top_students = (
        User.query
        .filter_by(college_id=college_id, role='student')
        .order_by(User.points.desc())
        .limit(10)
        .all()
    )

    return jsonify({
        'total_students': total_students,
        'active_students': active_students,
        'onboarded': onboarded,
        'top_students': [
            {'name': u.name, 'points': u.points, 'streak': u.streak}
            for u in top_students
        ],
    }), 200

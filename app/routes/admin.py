from datetime import datetime, timezone, timedelta
from flask import Blueprint, request, jsonify, g, current_app
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
    per_page = request.args.get('per_page', 50, type=int)
    search = request.args.get('search', '').strip()
    branch = request.args.get('branch', '').strip()
    section = request.args.get('section', '').strip()
    passout_year = request.args.get('passout_year', type=int)

    query = User.query.filter_by(college_id=college_id, role='student')
    if search:
        query = query.filter(
            (User.name.ilike(f'%{search}%')) | (User.email.ilike(f'%{search}%')) |
            (User.roll_number.ilike(f'%{search}%'))
        )
    if branch:
        query = query.filter_by(branch=branch)
    if section:
        query = query.filter_by(section=section)
    if passout_year:
        query = query.filter_by(passout_year=passout_year)

    pagination = query.order_by(User.points.desc()).paginate(page=page, per_page=per_page, error_out=False)

    students = []
    three_days_ago = datetime.now(timezone.utc) - timedelta(days=3)
    for u in pagination.items:
        d = u.to_dict()
        d['last_active'] = u.last_active.replace(tzinfo=timezone.utc).isoformat() if u.last_active else None
        d['is_inactive'] = (
            u.last_active is None or
            (u.last_active.replace(tzinfo=timezone.utc) if u.last_active.tzinfo is None else u.last_active) < three_days_ago
        ) if u.last_active else True
        students.append(d)

    return jsonify({
        'students': students,
        'total': pagination.total,
        'page': page,
        'pages': pagination.pages,
    }), 200


@admin_bp.get('/analytics')
@role_required('college_admin')
def get_analytics():
    college_id = g.current_user.college_id
    three_days_ago = datetime.now(timezone.utc) - timedelta(days=3)
    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)

    all_students = User.query.filter_by(college_id=college_id, role='student').all()
    total_students = len(all_students)

    active_this_week = sum(
        1 for u in all_students
        if u.last_active and (
            u.last_active.replace(tzinfo=timezone.utc) if u.last_active.tzinfo is None else u.last_active
        ) >= seven_days_ago
    )

    avg_streak = round(sum(u.streak for u in all_students) / total_students, 1) if total_students else 0
    avg_points = round(sum(u.points for u in all_students) / total_students) if total_students else 0

    inactive_students = []
    for u in all_students:
        if u.last_active is None:
            inactive_students.append(u)
        else:
            last = u.last_active.replace(tzinfo=timezone.utc) if u.last_active.tzinfo is None else u.last_active
            if last < three_days_ago:
                inactive_students.append(u)

    # Branch-wise avg points
    branch_map = {}
    for u in all_students:
        b = u.branch or 'Unknown'
        if b not in branch_map:
            branch_map[b] = {'total': 0, 'count': 0}
        branch_map[b]['total'] += u.points
        branch_map[b]['count'] += 1
    branch_stats = [
        {'branch': b, 'avgPoints': round(v['total'] / v['count']), 'count': v['count']}
        for b, v in branch_map.items() if v['count'] > 0
    ]
    branch_stats.sort(key=lambda x: x['avgPoints'], reverse=True)

    # Top students
    top_students = sorted(all_students, key=lambda u: u.points, reverse=True)[:10]

    return jsonify({
        'total_students': total_students,
        'active_this_week': active_this_week,
        'avg_streak': avg_streak,
        'avg_points': avg_points,
        'branch_stats': branch_stats,
        'inactive_students': [
            {
                'id': u.id,
                'name': u.name,
                'email': u.email,
                'branch': u.branch,
                'section': u.section,
                'roll_number': u.roll_number,
                'last_active': u.last_active.replace(tzinfo=timezone.utc).isoformat() if u.last_active else None,
            }
            for u in inactive_students
        ],
        'top_students': [
            {'id': u.id, 'name': u.name, 'points': u.points, 'streak': u.streak, 'branch': u.branch}
            for u in top_students
        ],
    }), 200


@admin_bp.get('/college-social')
@role_required('college_admin')
def get_college_social():
    college = g.current_user.college
    if not college:
        return jsonify({}), 200
    return jsonify({
        'linkedin_url': college.linkedin_url,
        'linkedin_post_embeds': college.linkedin_post_embeds or [],
        'instagram_url': college.instagram_url,
        'instagram_post_embeds': college.instagram_post_embeds or [],
    }), 200


@admin_bp.patch('/college-social')
@role_required('college_admin')
def update_college_social():
    college = g.current_user.college
    if not college:
        return jsonify({'error': 'College not found'}), 404

    data = request.get_json()
    import re as _re

    if 'linkedin_url' in data:
        college.linkedin_url = data['linkedin_url'] or None
    if 'linkedin_post_embeds' in data:
        embeds = data['linkedin_post_embeds']
        if isinstance(embeds, list):
            cleaned = []
            for u in embeds:
                if not u:
                    continue
                src_match = _re.search(r'src=["\']([^"\']+)["\']', u)
                if src_match:
                    cleaned.append(src_match.group(1))
                elif u.strip().startswith('http'):
                    cleaned.append(u.strip())
            college.linkedin_post_embeds = cleaned or None
        else:
            college.linkedin_post_embeds = None
    if 'instagram_url' in data:
        college.instagram_url = data['instagram_url'] or None
    if 'instagram_post_embeds' in data:
        embeds = data['instagram_post_embeds']
        if isinstance(embeds, list):
            cleaned = []
            for u in embeds:
                if not u:
                    continue
                src_match = _re.search(r'src=["\']([^"\']+)["\']', u)
                if src_match:
                    cleaned.append(src_match.group(1))
                elif u.strip().startswith('http'):
                    cleaned.append(u.strip())
            college.instagram_post_embeds = cleaned or None
        else:
            college.instagram_post_embeds = None

    db.session.commit()
    return jsonify({'message': 'Social links updated'}), 200


@admin_bp.post('/students/<int:student_id>/remind')
@role_required('college_admin')
def send_reminder(student_id):
    college_id = g.current_user.college_id
    student = User.query.filter_by(id=student_id, college_id=college_id, role='student').first()
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    try:
        from app.services.email_service import send_reminder_email
        send_reminder_email(student.email, student.name)
    except Exception as e:
        current_app.logger.error(f'Reminder email failed: {e}')

    return jsonify({'message': f'Reminder sent to {student.name}'}), 200

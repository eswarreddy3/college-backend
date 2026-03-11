import os
from flask import Blueprint, request, jsonify, g, current_app
from werkzeug.utils import secure_filename
from sqlalchemy import text
from app.extensions import db
from app.models.college import College
from app.models.user import User
from app.models.package import Package
from app.utils.decorators import role_required
from app.utils.helpers import hash_password, generate_activation_token
from app.services.email_service import send_activation_email, send_student_welcome_email
from app.services.csv_service import parse_student_csv

super_admin_bp = Blueprint('super_admin', __name__)

ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}


def _allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _purge_user_records(user_id):
    """Delete all FK-constrained rows referencing a user before deleting the user row.
    MySQL doesn't allow self-referencing subqueries directly, so subqueries are
    wrapped in an extra derived table alias to work around that restriction."""
    uid = {"uid": user_id}

    db.session.execute(text("DELETE FROM user_streaks WHERE user_id = :uid"), uid)
    db.session.execute(text("DELETE FROM user_lesson_progress WHERE user_id = :uid"), uid)
    db.session.execute(text("DELETE FROM mcq_attempts WHERE user_id = :uid"), uid)
    db.session.execute(text("DELETE FROM assignment_attempts WHERE user_id = :uid"), uid)
    db.session.execute(text("DELETE FROM coding_submissions WHERE user_id = :uid"), uid)

    # Likes this user gave (on any comment)
    db.session.execute(text("DELETE FROM comment_likes WHERE user_id = :uid"), uid)
    # Likes this user gave (on any post)
    db.session.execute(text("DELETE FROM post_likes WHERE user_id = :uid"), uid)

    # Posts owned by this user — clear comments + likes on those posts first
    db.session.execute(text(
        "DELETE FROM comment_likes WHERE comment_id IN "
        "(SELECT id FROM (SELECT id FROM comments "
        " WHERE post_id IN (SELECT id FROM (SELECT id FROM posts WHERE user_id = :uid) AS p)) AS c)"
    ), uid)
    db.session.execute(text(
        "DELETE FROM comments WHERE post_id IN "
        "(SELECT id FROM (SELECT id FROM posts WHERE user_id = :uid) AS sub)"
    ), uid)
    db.session.execute(text(
        "DELETE FROM post_likes WHERE post_id IN "
        "(SELECT id FROM (SELECT id FROM posts WHERE user_id = :uid) AS sub)"
    ), uid)
    db.session.execute(text("DELETE FROM posts WHERE user_id = :uid"), uid)

    # Comments by this user on other posts —
    # nullify replies that point to their comments, then remove likes, then remove comments
    db.session.execute(text(
        "UPDATE comments SET parent_id = NULL WHERE parent_id IN "
        "(SELECT id FROM (SELECT id FROM comments WHERE user_id = :uid) AS sub)"
    ), uid)
    db.session.execute(text(
        "DELETE FROM comment_likes WHERE comment_id IN "
        "(SELECT id FROM (SELECT id FROM comments WHERE user_id = :uid) AS sub)"
    ), uid)
    db.session.execute(text("DELETE FROM comments WHERE user_id = :uid"), uid)

    # Cascade-handled by ORM but explicit for safety
    db.session.execute(text("DELETE FROM refresh_tokens WHERE user_id = :uid"), uid)
    db.session.execute(text("DELETE FROM activity_logs WHERE user_id = :uid"), uid)


# --- Colleges ---

@super_admin_bp.get('/colleges')
@role_required('super_admin')
def list_colleges():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '').strip()
    status = request.args.get('status', '')

    query = College.query
    if search:
        query = query.filter(College.name.ilike(f'%{search}%'))
    if status == 'active':
        query = query.filter_by(is_active=True)
    elif status == 'inactive':
        query = query.filter_by(is_active=False)

    pagination = query.order_by(College.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'colleges': [c.to_dict() for c in pagination.items],
        'total': pagination.total,
        'page': page,
        'pages': pagination.pages,
    }), 200


@super_admin_bp.post('/colleges')
@role_required('super_admin')
def create_college():
    data = request.get_json(silent=True) or {}

    required = ['college_name', 'admin_name', 'admin_email']
    for field in required:
        if not data.get(field, '').strip():
            return jsonify({'error': f'{field} is required'}), 400

    # Check email uniqueness
    if User.query.filter_by(email=data['admin_email'].lower()).first():
        return jsonify({'error': 'Admin email already exists'}), 409

    activation_token = generate_activation_token()

    raw = data.get('allowed_domain_ids')
    allowed_domain_ids = raw if isinstance(raw, list) else None

    raw_c = data.get('allowed_course_ids')
    allowed_course_ids = raw_c if isinstance(raw_c, list) else None

    college = College(
        name=data['college_name'].strip(),
        location=data.get('location', '').strip(),
        package_id=data.get('package_id') or None,
        allowed_domain_ids=allowed_domain_ids,
        allowed_course_ids=allowed_course_ids,
        activation_token=activation_token,
        is_active=False,
    )
    db.session.add(college)
    db.session.flush()  # get college.id

    admin = User(
        name=data['admin_name'].strip(),
        email=data['admin_email'].strip().lower(),
        password_hash=hash_password(generate_activation_token()[:16]),  # temp password
        role='college_admin',
        college_id=college.id,
        is_active=False,
        first_login=True,
    )
    db.session.add(admin)
    db.session.commit()

    sent = send_activation_email(admin.email, admin.name, college.name, activation_token)
    email_warning = None if sent else "College created but activation email could not be sent. Use Resend Activation."

    return jsonify({
        'message': 'College created. Activation email sent.' if sent else email_warning,
        'college': college.to_dict(),
        'email_warning': email_warning,
    }), 201


@super_admin_bp.patch('/colleges/<int:college_id>')
@role_required('super_admin')
def update_college(college_id):
    college = College.query.get_or_404(college_id)
    data = request.get_json(silent=True) or {}

    if 'name' in data:
        college.name = data['name']
    if 'location' in data:
        college.location = data['location']
    if 'package_id' in data:
        college.package_id = data['package_id']
    if 'is_active' in data:
        new_status = bool(data['is_active'])
        college.is_active = new_status
        # Cascade to all users in this college
        User.query.filter_by(college_id=college.id).update({'is_active': new_status})
    if 'allowed_domain_ids' in data:
        ids = data['allowed_domain_ids']
        college.allowed_domain_ids = ids if isinstance(ids, list) else None
    if 'allowed_course_ids' in data:
        ids = data['allowed_course_ids']
        college.allowed_course_ids = ids if isinstance(ids, list) else None

    db.session.commit()
    return jsonify({'message': 'College updated', 'college': college.to_dict()}), 200


@super_admin_bp.delete('/colleges/<int:college_id>')
@role_required('super_admin')
def delete_college(college_id):
    college = College.query.get_or_404(college_id)

    # Purge every user's dependent rows first
    user_ids = [r[0] for r in db.session.execute(
        text("SELECT id FROM users WHERE college_id = :cid"), {"cid": college_id}
    ).fetchall()]
    for uid in user_ids:
        _purge_user_records(uid)

    # Clean up any college-scoped posts left (e.g. admin posts not caught above)
    cid = {"cid": college_id}
    db.session.execute(text(
        "DELETE FROM comment_likes WHERE comment_id IN "
        "(SELECT id FROM (SELECT id FROM comments "
        " WHERE post_id IN (SELECT id FROM (SELECT id FROM posts WHERE college_id = :cid) AS p)) AS c)"
    ), cid)
    db.session.execute(text(
        "DELETE FROM comments WHERE post_id IN "
        "(SELECT id FROM (SELECT id FROM posts WHERE college_id = :cid) AS sub)"
    ), cid)
    db.session.execute(text(
        "DELETE FROM post_likes WHERE post_id IN "
        "(SELECT id FROM (SELECT id FROM posts WHERE college_id = :cid) AS sub)"
    ), cid)
    db.session.execute(text("DELETE FROM posts WHERE college_id = :cid"), cid)

    db.session.execute(text("DELETE FROM users WHERE college_id = :cid"), cid)
    db.session.delete(college)
    db.session.commit()
    return jsonify({'message': 'College deleted'}), 200


@super_admin_bp.post('/colleges/<int:college_id>/resend-activation')
@role_required('super_admin')
def resend_activation(college_id):
    college = College.query.get_or_404(college_id)
    admin = User.query.filter_by(college_id=college_id, role='college_admin').first()
    if not admin:
        return jsonify({'error': 'No admin found for this college'}), 404

    activation_token = generate_activation_token()
    college.activation_token = activation_token
    db.session.commit()

    sent = send_activation_email(admin.email, admin.name, college.name, activation_token)
    if not sent:
        return jsonify({'error': 'Failed to send activation email. Check server mail configuration.'}), 500
    return jsonify({'message': 'Activation email resent'}), 200


# --- Students ---

@super_admin_bp.get('/students')
@role_required('super_admin')
def list_students():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '').strip()
    college_id = request.args.get('college_id', type=int)

    query = User.query.filter_by(role='student')
    if search:
        query = query.filter(
            (User.name.ilike(f'%{search}%')) | (User.email.ilike(f'%{search}%'))
        )
    if college_id:
        query = query.filter_by(college_id=college_id)

    pagination = query.order_by(User.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'students': [u.to_dict() for u in pagination.items],
        'total': pagination.total,
        'page': page,
        'pages': pagination.pages,
    }), 200


@super_admin_bp.post('/students')
@role_required('super_admin')
def create_student():
    data = request.get_json(silent=True) or {}

    required = ['name', 'email', 'college_id']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400

    if User.query.filter_by(email=data['email'].lower()).first():
        return jsonify({'error': 'Email already exists'}), 409

    college = College.query.get(data['college_id'])
    if not college:
        return jsonify({'error': 'College not found'}), 404

    import secrets
    temp_password = secrets.token_urlsafe(8)

    student = User(
        name=data['name'].strip(),
        email=data['email'].strip().lower(),
        password_hash=hash_password(temp_password),
        role='student',
        college_id=data['college_id'],
        branch=data.get('branch', ''),
        section=data.get('section', ''),
        roll_number=data.get('roll_number', ''),
        passout_year=data.get('passout_year'),
        is_active=True,
        first_login=True,
    )
    db.session.add(student)
    db.session.commit()

    send_student_welcome_email(student.email, student.name, temp_password)

    return jsonify({'message': 'Student created', 'student': student.to_dict()}), 201


@super_admin_bp.patch('/students/<int:student_id>')
@role_required('super_admin')
def update_student(student_id):
    student = User.query.filter_by(id=student_id, role='student').first_or_404()
    data = request.get_json(silent=True) or {}
    if 'is_active' in data:
        student.is_active = bool(data['is_active'])
    db.session.commit()
    return jsonify({'message': 'Student updated', 'student': student.to_dict()}), 200


@super_admin_bp.delete('/students/<int:student_id>')
@role_required('super_admin')
def delete_student(student_id):
    student = User.query.filter_by(id=student_id, role='student').first_or_404()
    _purge_user_records(student_id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted'}), 200


@super_admin_bp.post('/students/bulk-upload')
@role_required('super_admin')
def bulk_upload_students():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    college_id = request.form.get('college_id', type=int)

    if not file.filename or not _allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Use CSV or XLSX.'}), 400

    if not college_id:
        return jsonify({'error': 'college_id is required'}), 400

    college = College.query.get(college_id)
    if not college:
        return jsonify({'error': 'College not found'}), 404

    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    try:
        students_data, errors = parse_student_csv(file_path)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

    if errors and not students_data:
        return jsonify({'error': 'CSV parsing failed', 'details': errors}), 400

    created = []
    skipped = []
    for s in students_data:
        if User.query.filter_by(email=s['email']).first():
            skipped.append(s['email'])
            continue

        student = User(
            name=s['name'],
            email=s['email'],
            password_hash=hash_password(s['temp_password']),
            role='student',
            college_id=college_id,
            branch=s['branch'],
            section=s['section'],
            roll_number=s['roll_number'],
            passout_year=s['passout_year'],
            is_active=True,
            first_login=True,
        )
        db.session.add(student)
        created.append(s['email'])
        send_student_welcome_email(s['email'], s['name'], s['temp_password'])

    db.session.commit()

    return jsonify({
        'message': f'{len(created)} students created, {len(skipped)} skipped (already exist)',
        'created': len(created),
        'skipped': skipped,
        'parse_errors': errors,
    }), 201


# --- Courses (for super-admin course selector) ---

@super_admin_bp.get('/courses')
@role_required('super_admin')
def list_courses():
    from app.models.learn import Course
    courses = Course.query.filter_by(is_active=True).order_by(Course.order).all()
    return jsonify([{'id': c.id, 'title': c.title, 'category': c.category, 'icon_color': c.icon_color} for c in courses]), 200


# --- Packages ---

@super_admin_bp.get('/packages')
@role_required('super_admin')
def list_packages():
    packages = Package.query.filter_by(is_active=True).all()
    return jsonify([p.to_dict() for p in packages]), 200


@super_admin_bp.patch('/packages/<int:package_id>')
@role_required('super_admin')
def update_package(package_id):
    package = Package.query.get_or_404(package_id)
    data = request.get_json(silent=True) or {}

    if 'price' in data:
        package.price = float(data['price'])
    if 'features' in data:
        package.features = data['features']
    if 'name' in data:
        package.name = data['name']

    db.session.commit()
    return jsonify({'message': 'Package updated', 'package': package.to_dict()}), 200


# --- Overview stats ---

@super_admin_bp.get('/overview')
@role_required('super_admin')
def overview():
    total_colleges = College.query.count()
    total_students = User.query.filter_by(role='student').count()
    total_packages = Package.query.filter_by(is_active=True).count()
    pending = College.query.filter_by(is_active=False).count()

    return jsonify({
        'total_colleges': total_colleges,
        'total_students': total_students,
        'total_packages': total_packages,
        'pending_verifications': pending,
    }), 200

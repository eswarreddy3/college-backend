import os
from flask import Blueprint, request, jsonify, g, current_app
from werkzeug.utils import secure_filename
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

    college = College(
        name=data['college_name'].strip(),
        location=data.get('location', '').strip(),
        package_id=data.get('package_id') or None,
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

    send_activation_email(admin.email, admin.name, college.name, activation_token)

    return jsonify({'message': 'College created. Activation email sent.', 'college': college.to_dict()}), 201


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
        college.is_active = data['is_active']

    db.session.commit()
    return jsonify({'message': 'College updated', 'college': college.to_dict()}), 200


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

    send_activation_email(admin.email, admin.name, college.name, activation_token)
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

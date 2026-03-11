from flask import Blueprint, jsonify, g
from app.extensions import db
from app.models.domain import Domain, DomainCourse
from app.models.learn import Course, UserLessonProgress
from app.utils.decorators import jwt_required

domain_programs_bp = Blueprint('domain_programs', __name__)


@domain_programs_bp.get('/')
@jwt_required
def list_domains():
    """Return all active domains with summary stats. Marks locked domains based on college's allowed_domain_ids."""
    domains = Domain.query.filter_by(is_active=True).order_by(Domain.order).all()

    college = g.current_user.college
    allowed_ids = college.allowed_domain_ids if college else None  # None = all accessible

    result = []
    for d in domains:
        d_dict = d.to_dict()
        d_dict['is_locked'] = bool(allowed_ids is not None and d.id not in allowed_ids)
        result.append(d_dict)

    return jsonify(result), 200


@domain_programs_bp.get('/<domain_id>/courses')
@jwt_required
def get_domain_courses(domain_id):
    """Return courses for a domain with user progress, ordered by domain order_index."""
    domain = Domain.query.filter_by(id=domain_id, is_active=True).first()
    if not domain:
        return jsonify({'error': 'Domain not found'}), 404

    college = g.current_user.college
    allowed_ids = college.allowed_domain_ids if college else None
    if allowed_ids is not None and domain_id not in allowed_ids:
        return jsonify({'error': 'This domain is not available in your college plan'}), 403

    user_id = g.current_user.id

    # Completed lesson IDs for this user
    completed_lesson_ids = {
        p.lesson_id
        for p in UserLessonProgress.query.filter_by(user_id=user_id).all()
    }

    # Which courses has the user fully completed? (needed for prerequisite locking)
    all_courses = Course.query.filter_by(is_active=True).all()
    completed_courses = set()
    for c in all_courses:
        active_lessons = [l for l in c.lessons if l.is_active]
        if active_lessons and all(l.id in completed_lesson_ids for l in active_lessons):
            completed_courses.add(c.id)

    result = []
    for dc in domain.domain_courses:
        course = dc.course
        if not course or not course.is_active:
            continue

        lessons_completed = sum(
            1 for l in course.lessons if l.is_active and l.id in completed_lesson_ids
        )
        is_locked = bool(course.prerequisite_id and course.prerequisite_id not in completed_courses)

        course_data = course.to_dict(lessons_completed=lessons_completed, is_locked=is_locked)
        course_data['order_index'] = dc.order_index
        result.append(course_data)

    return jsonify({
        'domain': domain.to_dict(),
        'courses': result,
    }), 200

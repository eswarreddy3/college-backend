from flask import Blueprint, request, jsonify, g
from app.extensions import db
from app.models.learn import Course, Lesson, UserLessonProgress
from app.models.activity_log import ActivityLog
from app.utils.decorators import jwt_required
from app.utils.helpers import update_streak

learn_bp = Blueprint('learn', __name__)


@learn_bp.get('/courses')
@jwt_required
def get_courses():
    """Return all active courses with the user's lesson completion counts."""
    user_id = g.current_user.id

    courses = Course.query.filter_by(is_active=True).order_by(Course.order).all()

    # Completed lesson IDs for this user
    completed = {
        p.lesson_id
        for p in UserLessonProgress.query.filter_by(user_id=user_id).all()
    }

    # Which courses are unlocked: course is locked if its prerequisite has 0 completions
    # Build a set of course IDs where user completed ALL lessons
    completed_courses = set()
    for c in courses:
        active_lessons = [l for l in c.lessons if l.is_active]
        if active_lessons and all(l.id in completed for l in active_lessons):
            completed_courses.add(c.id)

    result = []
    for c in courses:
        lessons_completed = sum(
            1 for l in c.lessons if l.is_active and l.id in completed
        )
        is_locked = bool(c.prerequisite_id and c.prerequisite_id not in completed_courses)
        result.append(c.to_dict(lessons_completed=lessons_completed, is_locked=is_locked))

    return jsonify(result), 200


@learn_bp.get('/courses/<course_id>')
@jwt_required
def get_course(course_id):
    """Return a single course with all its lessons and user completion state."""
    user_id = g.current_user.id

    course = Course.query.filter_by(id=course_id, is_active=True).first()
    if not course:
        return jsonify({'error': 'Course not found'}), 404

    completed = {
        p.lesson_id
        for p in UserLessonProgress.query.filter_by(user_id=user_id).all()
    }

    lessons_data = [
        l.to_dict(is_completed=(l.id in completed))
        for l in course.lessons if l.is_active
    ]

    lessons_completed = sum(1 for l in lessons_data if l['is_completed'])

    data = course.to_dict(lessons_completed=lessons_completed)
    data['lessons'] = lessons_data
    return jsonify(data), 200


@learn_bp.post('/lessons/<int:lesson_id>/complete')
@jwt_required
def complete_lesson(lesson_id):
    """Mark a lesson as complete and award points (idempotent)."""
    user = g.current_user

    lesson = Lesson.query.get(lesson_id)
    if not lesson or not lesson.is_active:
        return jsonify({'error': 'Lesson not found'}), 404

    existing = UserLessonProgress.query.filter_by(
        user_id=user.id, lesson_id=lesson_id
    ).first()

    if existing:
        return jsonify({
            'already_completed': True,
            'points_earned': 0,
            'total_points': user.points,
        }), 200

    progress = UserLessonProgress(
        user_id=user.id,
        lesson_id=lesson_id,
        points_earned=lesson.points,
    )
    db.session.add(progress)

    user.points += lesson.points

    log = ActivityLog(
        user_id=user.id,
        action=f'Completed lesson: {lesson.title[:50]}',
        details={'description': lesson.course.title, 'points': lesson.points},
    )
    db.session.add(log)
    update_streak(user.id)
    db.session.commit()

    return jsonify({
        'already_completed': False,
        'points_earned': lesson.points,
        'total_points': user.points,
    }), 200

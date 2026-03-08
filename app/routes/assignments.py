from flask import Blueprint, request, jsonify, g
from app.extensions import db
from app.models.assignment import AssignmentQuestion, AssignmentAttempt
from app.models.activity_log import ActivityLog
from app.utils.decorators import jwt_required

assignments_bp = Blueprint('assignments', __name__)

# Static metadata per module — title, course, duration, icon, due date
MODULE_META = {
    'python-basics': {
        'title': 'Python Basics Assessment',
        'course': 'Python',
        'duration_mins': 20,
        'icon': '🌱',
        'due_date': 'Mar 20, 2026',
    },
    'python-intermediate': {
        'title': 'Python Intermediate Assessment',
        'course': 'Python',
        'duration_mins': 25,
        'icon': '⚙️',
        'due_date': 'Mar 25, 2026',
    },
    'python-advanced': {
        'title': 'Python Advanced Assessment',
        'course': 'Python',
        'duration_mins': 30,
        'icon': '🚀',
        'due_date': 'Apr 01, 2026',
    },
    '1': {
        'title': 'Python Basics Assessment',
        'course': 'Python',
        'duration_mins': 30,
        'icon': '🐍',
        'due_date': 'Mar 10, 2026',
    },
    '2': {
        'title': 'SQL Joins & Queries',
        'course': 'Database Management',
        'duration_mins': 25,
        'icon': '🗄️',
        'due_date': 'Mar 15, 2026',
    },
    '3': {
        'title': 'Data Structures Challenge',
        'course': 'Computer Science',
        'duration_mins': 30,
        'icon': '🌳',
        'due_date': 'Mar 18, 2026',
    },
    '4': {
        'title': 'Aptitude & Reasoning Test',
        'course': 'Aptitude',
        'duration_mins': 20,
        'icon': '🧮',
        'due_date': 'Mar 22, 2026',
    },
    '5': {
        'title': 'JavaScript Fundamentals',
        'course': 'Web Development',
        'duration_mins': 25,
        'icon': '🌐',
        'due_date': 'Mar 28, 2026',
    },
}


@assignments_bp.get('/list')
@jwt_required
def list_assignments():
    """Return all assignment modules with user completion status."""
    user_id = g.current_user.id

    # Get user's attempts indexed by module_id (latest per module)
    attempts = {}
    for a in AssignmentAttempt.query.filter_by(user_id=user_id).all():
        if a.module_id not in attempts or a.completed_at > attempts[a.module_id].completed_at:
            attempts[a.module_id] = a

    # Get question counts per module
    from sqlalchemy import func
    counts = dict(
        db.session.query(AssignmentQuestion.module_id, func.count(AssignmentQuestion.id))
        .filter_by(is_active=True)
        .group_by(AssignmentQuestion.module_id)
        .all()
    )

    result = []
    for module_id, meta in MODULE_META.items():
        total_q = counts.get(module_id, 0)
        attempt = attempts.get(module_id)

        max_score = total_q * 5  # 5 pts per question

        if attempt:
            status = 'completed'
            completed_questions = attempt.total_questions
            score = attempt.score
        else:
            status = 'pending'
            completed_questions = 0
            score = 0

        result.append({
            'id': module_id,
            'module_id': module_id,
            'title': meta['title'],
            'course': meta['course'],
            'icon': meta['icon'],
            'due_date': meta['due_date'],
            'duration_mins': meta['duration_mins'],
            'total_questions': total_q,
            'completed_questions': completed_questions,
            'status': status,
            'points': max_score,
            'score': score,
        })

    return jsonify(result), 200


@assignments_bp.get('/<module_id>/questions')
@jwt_required
def get_questions(module_id):
    """Return all questions for an assignment module."""
    if module_id not in MODULE_META:
        return jsonify({'error': 'Assignment not found'}), 404

    questions = (
        AssignmentQuestion.query
        .filter_by(module_id=module_id, is_active=True)
        .order_by(AssignmentQuestion.id)
        .all()
    )

    if not questions:
        return jsonify({'error': 'No questions found for this module'}), 404

    meta = MODULE_META[module_id]
    return jsonify({
        'assignment': {
            'id': module_id,
            'module_id': module_id,
            'title': meta['title'],
            'course': meta['course'],
            'icon': meta['icon'],
            'duration_mins': meta['duration_mins'],
            'total_questions': len(questions),
            'points': len(questions) * 5,
        },
        'questions': [q.to_dict() for q in questions],  # no correct_answer
    }), 200


@assignments_bp.post('/<module_id>/submit')
@jwt_required
def submit_assignment(module_id):
    """Submit assignment answers, evaluate, award points."""
    if module_id not in MODULE_META:
        return jsonify({'error': 'Assignment not found'}), 404

    user = g.current_user
    data = request.get_json(silent=True) or {}
    answers = data.get('answers', {})  # {str(question_id): selected_index}

    questions = (
        AssignmentQuestion.query
        .filter_by(module_id=module_id, is_active=True)
        .order_by(AssignmentQuestion.id)
        .all()
    )

    if not questions:
        return jsonify({'error': 'No questions found'}), 404

    # Evaluate
    results = []
    correct_count = 0
    score = 0

    for q in questions:
        selected = answers.get(str(q.id))
        if selected is None:
            selected_idx = -1
            is_correct = False
        else:
            selected_idx = int(selected)
            is_correct = (selected_idx == q.correct_answer)

        if is_correct:
            correct_count += 1
            score += q.points

        results.append({
            'id': q.id,
            'question': q.question,
            'options': q.options,
            'correctIndex': q.correct_answer,
            'selectedIndex': selected_idx,
            'explanation': q.explanation or '',
            'isCorrect': is_correct,
            'subtopic': q.subtopic,
        })

    total_q = len(questions)
    wrong = sum(1 for r in results if not r['isCorrect'] and r['selectedIndex'] != -1)
    unanswered = sum(1 for r in results if r['selectedIndex'] == -1)

    # Save attempt
    attempt = AssignmentAttempt(
        user_id=user.id,
        module_id=module_id,
        score=score,
        total_questions=total_q,
        correct_count=correct_count,
        answers={str(q.id): answers.get(str(q.id)) for q in questions},
    )
    db.session.add(attempt)

    # Award points to user
    user.points += score

    # Log activity
    meta = MODULE_META[module_id]
    log = ActivityLog(
        user_id=user.id,
        action=f'Completed Assignment: {meta["title"]}',
        details={
            'description': f'{correct_count}/{total_q} correct — {meta["course"]}',
            'points': score,
        },
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({
        'assignmentId': module_id,
        'title': meta['title'],
        'course': meta['course'],
        'correct': correct_count,
        'wrong': wrong,
        'unanswered': unanswered,
        'score': score,
        'maxScore': total_q * 5,
        'total_points': user.points,
        'results': results,
    }), 200

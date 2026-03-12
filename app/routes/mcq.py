from flask import Blueprint, request, jsonify, g
from app.extensions import db
from app.models.mcq import MCQQuestion, MCQAttempt
from app.models.aptitude import AptitudeQuestion, AptitudeAttempt
from app.models.activity_log import ActivityLog
from app.utils.decorators import jwt_required
from app.utils.helpers import update_streak

mcq_bp = Blueprint('mcq', __name__)


@mcq_bp.get('/topics')
@jwt_required
def get_topics():
    """Return topics with subtopics and question counts, plus user's attempt counts."""
    user_id = g.current_user.id

    # All active questions grouped
    questions = MCQQuestion.query.filter_by(is_active=True).all()

    # Questions the user already answered correctly (no re-earning points)
    attempted_ids = {
        a.question_id for a in MCQAttempt.query.filter_by(user_id=user_id).all()
    }

    # Build topic → subtopic tree
    tree: dict = {}
    for q in questions:
        if q.topic not in tree:
            tree[q.topic] = {}
        if q.subtopic not in tree[q.topic]:
            tree[q.topic][q.subtopic] = {'total': 0, 'attempted': 0}
        tree[q.topic][q.subtopic]['total'] += 1
        if q.id in attempted_ids:
            tree[q.topic][q.subtopic]['attempted'] += 1

    result = []
    for topic, subtopics in tree.items():
        result.append({
            'topic': topic,
            'subtopics': [
                {
                    'name': sub,
                    'total': data['total'],
                    'attempted': data['attempted'],
                }
                for sub, data in subtopics.items()
            ],
        })

    return jsonify(result), 200


@mcq_bp.get('/questions')
@jwt_required
def get_questions():
    """Get questions for a topic/subtopic."""
    topic = request.args.get('topic', '')
    subtopic = request.args.get('subtopic', '')

    query = MCQQuestion.query.filter_by(is_active=True)
    if topic:
        query = query.filter_by(topic=topic)
    if subtopic:
        query = query.filter_by(subtopic=subtopic)

    questions = query.order_by(MCQQuestion.id).all()

    # Get user's attempts for these questions
    qids = [q.id for q in questions]
    attempts = {
        a.question_id: a
        for a in MCQAttempt.query.filter(
            MCQAttempt.user_id == g.current_user.id,
            MCQAttempt.question_id.in_(qids)
        ).all()
    } if qids else {}

    result = []
    for q in questions:
        d = q.to_dict()
        if q.id in attempts:
            a = attempts[q.id]
            d['attempted'] = True
            d['selected_answer'] = a.selected_answer
            d['is_correct'] = a.is_correct
            d['correct_answer'] = q.correct_answer  # reveal after attempt
        else:
            d['attempted'] = False
        result.append(d)

    return jsonify(result), 200


@mcq_bp.post('/answer')
@jwt_required
def submit_answer():
    """Submit an answer for a question."""
    user = g.current_user
    data = request.get_json(silent=True) or {}

    question_id = data.get('question_id')
    selected_answer = data.get('selected_answer')

    if question_id is None or selected_answer is None:
        return jsonify({'error': 'question_id and selected_answer are required'}), 400

    question = MCQQuestion.query.get(question_id)
    if not question or not question.is_active:
        return jsonify({'error': 'Question not found'}), 404

    is_correct = (selected_answer == question.correct_answer)
    points_earned = 0

    # Check if already attempted
    existing = MCQAttempt.query.filter_by(user_id=user.id, question_id=question_id).first()
    if existing:
        prev_points = existing.points_earned or 0
        existing.selected_answer = selected_answer
        existing.is_correct = is_correct

        if is_correct:
            # Correct on retry — award points only if none earned yet
            if prev_points == 0:
                points_earned = question.points
                existing.points_earned = points_earned
                user.points += points_earned
                log = ActivityLog(
                    user_id=user.id,
                    action=f'Answered MCQ: {question.subtopic}',
                    details={'description': question.question[:60] + '...', 'points': points_earned},
                )
                db.session.add(log)
            # else: already earned, no change
        else:
            # Wrong on retry — reclaim points if previously earned
            if prev_points > 0:
                user.points = max(0, user.points - prev_points)
            existing.points_earned = 0
    else:
        points_earned = question.points if is_correct else 0
        attempt = MCQAttempt(
            user_id=user.id,
            question_id=question_id,
            selected_answer=selected_answer,
            is_correct=is_correct,
            points_earned=points_earned,
        )
        db.session.add(attempt)

        if is_correct and points_earned > 0:
            user.points += points_earned
            log = ActivityLog(
                user_id=user.id,
                action=f'Answered MCQ: {question.subtopic}',
                details={'description': question.question[:60] + '...', 'points': points_earned},
            )
            db.session.add(log)

    update_streak(user.id)
    db.session.commit()

    return jsonify({
        'correct': is_correct,
        'correct_answer': question.correct_answer,
        'total_points': user.points,
        'explanation': question.explanation,
        'points_earned': points_earned,
    }), 200


# ── Aptitude Practice Routes ──────────────────────────────────────────────────

@mcq_bp.get('/aptitude/topics')
@jwt_required
def get_aptitude_topics():
    """Return aptitude topics with total question count and user's correctly answered count."""
    user_id = g.current_user.id

    correct_ids = {
        a.question_id
        for a in AptitudeAttempt.query.filter_by(user_id=user_id).all()
    }

    from sqlalchemy import func
    rows = (
        db.session.query(AptitudeQuestion.topic_name, func.count(AptitudeQuestion.id))
        .group_by(AptitudeQuestion.topic_name)
        .order_by(AptitudeQuestion.topic_name)
        .all()
    )

    # For answered count, fetch all questions once
    all_questions = AptitudeQuestion.query.all()
    topic_correct: dict = {}
    for q in all_questions:
        if q.id in correct_ids:
            topic_correct[q.topic_name] = topic_correct.get(q.topic_name, 0) + 1

    result = [
        {
            'topic_name': topic,
            'total': total,
            'answered': topic_correct.get(topic, 0),
        }
        for topic, total in rows
    ]
    return jsonify(result), 200


@mcq_bp.get('/aptitude/questions')
@jwt_required
def get_aptitude_questions():
    """Return paginated aptitude questions (5 per page) for a topic."""
    user_id = g.current_user.id
    topic = request.args.get('topic', '')
    page = max(1, int(request.args.get('page', 1)))
    page_size = 5

    query = AptitudeQuestion.query
    if topic:
        query = query.filter_by(topic_name=topic)
    query = query.order_by(AptitudeQuestion.id)

    total = query.count()
    total_pages = max(1, -(-total // page_size))  # ceiling division
    questions = query.offset((page - 1) * page_size).limit(page_size).all()

    correct_ids = {
        a.question_id
        for a in AptitudeAttempt.query.filter_by(user_id=user_id).all()
    }

    result = []
    for q in questions:
        d = q.to_dict()
        d['already_correct'] = q.id in correct_ids
        result.append(d)

    return jsonify({
        'questions': result,
        'page': page,
        'total_pages': total_pages,
        'total': total,
    }), 200


@mcq_bp.post('/aptitude/answer')
@jwt_required
def submit_aptitude_answer():
    """Submit an aptitude practice answer. 1 point per correct, unlimited retries."""
    user = g.current_user
    data = request.get_json(silent=True) or {}

    question_id = data.get('question_id')
    selected_answer = data.get('selected_answer')  # 'A', 'B', 'C', or 'D'

    if not question_id or not selected_answer:
        return jsonify({'error': 'question_id and selected_answer are required'}), 400

    question = AptitudeQuestion.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404

    is_correct = (selected_answer.upper() == question.correct_answer)
    points_earned = 0

    if is_correct:
        existing = AptitudeAttempt.query.filter_by(
            user_id=user.id, question_id=question_id
        ).first()
        if not existing:
            db.session.add(AptitudeAttempt(user_id=user.id, question_id=question_id))
            user.points += 1
            points_earned = 1
            update_streak(user.id)
        db.session.commit()

    return jsonify({
        'correct': is_correct,
        'correct_answer': question.correct_answer,
        'explanation': question.explanation,
        'points_earned': points_earned,
        'total_points': user.points,
    }), 200

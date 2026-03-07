from flask import Blueprint, request, jsonify, g
from app.extensions import db
from app.models.coding_problem import CodingProblem, CodingSubmission
from app.utils.decorators import jwt_required
from datetime import datetime, timezone
import random

coding_bp = Blueprint('coding', __name__)


@coding_bp.get('/problems')
@jwt_required
def list_problems():
    difficulty = request.args.get('difficulty', '')
    tag = request.args.get('tag', '')

    query = CodingProblem.query.filter_by(is_active=True)
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    if tag:
        query = query.filter(CodingProblem.tags.contains([tag]))

    problems = query.order_by(CodingProblem.id).all()
    return jsonify([p.to_dict() for p in problems]), 200


@coding_bp.get('/problems/<slug>')
@jwt_required
def get_problem(slug):
    problem = CodingProblem.query.filter_by(slug=slug, is_active=True).first_or_404()
    return jsonify(problem.to_dict(include_test_cases=False)), 200


@coding_bp.get('/problems/<slug>/submissions')
@jwt_required
def get_submissions(slug):
    problem = CodingProblem.query.filter_by(slug=slug, is_active=True).first_or_404()
    submissions = (
        CodingSubmission.query
        .filter_by(user_id=g.current_user.id, problem_id=problem.id)
        .order_by(CodingSubmission.submitted_at.desc())
        .limit(20)
        .all()
    )
    return jsonify([s.to_dict() for s in submissions]), 200


@coding_bp.post('/run')
@jwt_required
def run_code():
    data = request.get_json(silent=True) or {}
    # In a real implementation, this would execute code in a sandbox.
    # For now, return a simulated response.
    code = data.get('code', '')
    language = data.get('language', 'python')

    if not code.strip():
        return jsonify({'error': 'No code provided'}), 400

    # Simulated test run
    return jsonify({
        'status': 'success',
        'output': 'Test cases passed: 3/3\nRuntime: 45ms\nMemory: 14.2 MB',
        'test_results': [
            {'input': 'nums = [2,7,11,15], target = 9', 'expected': '[0,1]', 'got': '[0,1]', 'passed': True},
            {'input': 'nums = [3,2,4], target = 6', 'expected': '[1,2]', 'got': '[1,2]', 'passed': True},
            {'input': 'nums = [3,3], target = 6', 'expected': '[0,1]', 'got': '[0,1]', 'passed': True},
        ],
    }), 200


@coding_bp.post('/submit')
@jwt_required
def submit_code():
    user = g.current_user
    data = request.get_json(silent=True) or {}

    code = data.get('code', '')
    language = data.get('language', 'python')
    problem_slug = data.get('problem_slug', '')

    if not code.strip():
        return jsonify({'error': 'No code provided'}), 400

    problem = None
    if problem_slug:
        problem = CodingProblem.query.filter_by(slug=problem_slug).first()

    # Simulated submission evaluation
    statuses = ['accepted', 'wrong_answer', 'accepted', 'accepted']
    status = random.choice(statuses)
    runtime_ms = random.randint(30, 300)

    if problem:
        submission = CodingSubmission(
            user_id=user.id,
            problem_id=problem.id,
            language=language,
            code=code,
            status=status,
            runtime_ms=runtime_ms,
        )
        db.session.add(submission)

        # Award points on first accepted submission
        if status == 'accepted':
            existing_accepted = CodingSubmission.query.filter_by(
                user_id=user.id, problem_id=problem.id, status='accepted'
            ).count()
            if existing_accepted == 1:  # this one just added
                difficulty_points = {'Easy': 10, 'Medium': 25, 'Hard': 50}
                user.points += difficulty_points.get(problem.difficulty, 10)

        db.session.commit()

    return jsonify({
        'status': status,
        'runtime_ms': runtime_ms,
        'message': 'Accepted! Great job!' if status == 'accepted' else 'Wrong answer. Check your logic.',
    }), 200

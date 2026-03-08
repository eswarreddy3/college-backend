from flask import Blueprint, request, jsonify, g
from app.extensions import db
from app.models.coding_problem import CodingProblem, CodingSubmission
from app.models.activity_log import ActivityLog
from app.utils.decorators import jwt_required
from app.utils.executor import execute, run_test_cases
from datetime import datetime, timezone

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
    """Run code against sample test cases (visible). Does NOT save to DB."""
    data = request.get_json(silent=True) or {}
    code = data.get('code', '').strip()
    language = data.get('language', 'python')
    problem_slug = data.get('problem_slug', '')
    custom_input = data.get('custom_input', None)  # optional custom stdin

    if not code:
        return jsonify({'error': 'No code provided'}), 400

    # Custom input mode — just run code with given stdin
    if custom_input is not None:
        result = execute(language, code, custom_input)
        return jsonify({
            'status': 'success' if result.success else 'error',
            'output': result.stdout if result.success else result.stderr,
            'error': result.error,
            'runtime_ms': result.runtime_ms,
            'test_results': [],
        }), 200

    # Problem mode — run against first 3 visible test cases
    problem = CodingProblem.query.filter_by(slug=problem_slug, is_active=True).first()
    if not problem or not problem.test_cases:
        return jsonify({'error': 'Problem or test cases not found'}), 404

    # Use first 3 test cases for "run"
    sample_cases = (problem.test_cases or [])[:3]
    results = run_test_cases(language, code, sample_cases)

    all_passed = all(r['passed'] for r in results)
    passed_count = sum(1 for r in results if r['passed'])

    return jsonify({
        'status': 'passed' if all_passed else 'failed',
        'output': f'Test cases passed: {passed_count}/{len(results)}',
        'test_results': results,
    }), 200


@coding_bp.post('/submit')
@jwt_required
def submit_code():
    """Submit code against all test cases. Saves submission to DB."""
    user = g.current_user
    data = request.get_json(silent=True) or {}
    code = data.get('code', '').strip()
    language = data.get('language', 'python')
    problem_slug = data.get('problem_slug', '')

    if not code:
        return jsonify({'error': 'No code provided'}), 400

    problem = CodingProblem.query.filter_by(slug=problem_slug, is_active=True).first()
    if not problem:
        return jsonify({'error': 'Problem not found'}), 404

    if not problem.test_cases:
        return jsonify({'error': 'No test cases configured for this problem'}), 422

    # Run against ALL test cases
    all_cases = problem.test_cases or []
    results = run_test_cases(language, code, all_cases)

    passed_count = sum(1 for r in results if r['passed'])
    total = len(results)

    # Determine submission status
    if all(r['error'] == 'timeout' for r in results):
        status = 'time_limit'
    elif any(r['error'] in ('compile_error', 'runtime_error') for r in results):
        status = 'runtime_error'
    elif passed_count == total:
        status = 'accepted'
    else:
        status = 'wrong_answer'

    avg_runtime = int(sum(r['runtime_ms'] for r in results) / len(results)) if results else None

    # Save submission
    submission = CodingSubmission(
        user_id=user.id,
        problem_id=problem.id,
        language=language,
        code=code,
        status=status,
        runtime_ms=avg_runtime,
    )
    db.session.add(submission)

    # Award points on first accepted submission
    if status == 'accepted':
        prev_accepted = CodingSubmission.query.filter_by(
            user_id=user.id, problem_id=problem.id, status='accepted'
        ).count()
        if prev_accepted == 0:  # this is the first accepted (not yet committed)
            points = problem.points or 10
            user.points += points
            log = ActivityLog(
                user_id=user.id,
                action=f'Solved: {problem.title}',
                details={
                    'description': f'{problem.difficulty} — {", ".join(problem.tags or [])}',
                    'points': points,
                },
            )
            db.session.add(log)

    db.session.commit()

    points_awarded = 0
    if status == 'accepted':
        prev_accepted_count = CodingSubmission.query.filter_by(
            user_id=user.id, problem_id=problem.id, status='accepted'
        ).count()
        if prev_accepted_count == 1:  # just saved = first accepted
            points_awarded = problem.points or 10

    if status == 'accepted':
        msg_pts = f' +{points_awarded} pts' if points_awarded else ' (already solved)'
        message = f'All {total}/{total} test cases passed!{msg_pts}'
    elif status == 'wrong_answer':
        message = f'{passed_count}/{total} test cases passed.'
    elif status == 'runtime_error':
        failed = next((r for r in results if r['error']), None)
        message = f'Runtime error: {failed["got"][:200]}' if failed else 'Runtime error'
    elif status == 'time_limit':
        message = f'Time limit exceeded ({len(results)} test cases)'
    else:
        message = 'Submission failed'

    return jsonify({
        'status': status,
        'runtime_ms': avg_runtime,
        'passed': passed_count,
        'total': total,
        'message': message,
        'points_awarded': points_awarded,
        'total_user_points': user.points,
        'test_results': results,
    }), 200

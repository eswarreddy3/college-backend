from datetime import datetime, timezone
from app.extensions import db


class CodingProblem(db.Model):
    __tablename__ = 'coding_problems'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.Enum('Easy', 'Medium', 'Hard'), default='Easy')
    tags = db.Column(db.JSON, default=list)
    examples = db.Column(db.JSON, default=list)
    constraints = db.Column(db.Text, nullable=True)
    starter_code = db.Column(db.JSON, default=dict)  # {python: "...", java: "..."}
    test_cases = db.Column(db.JSON, default=list)
    points = db.Column(db.Integer, default=10)       # points awarded on first accepted submission
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    submissions = db.relationship('CodingSubmission', backref='problem', lazy=True)

    def to_dict(self, include_test_cases=False):
        data = {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'description': self.description,
            'difficulty': self.difficulty,
            'tags': self.tags or [],
            'examples': self.examples or [],
            'constraints': self.constraints,
            'starter_code': self.starter_code or {},
            'points': self.points or 10,
        }
        if include_test_cases:
            data['test_cases'] = self.test_cases or []
        return data


class CodingSubmission(db.Model):
    __tablename__ = 'coding_submissions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey('coding_problems.id'), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    code = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum('accepted', 'wrong_answer', 'runtime_error', 'time_limit'), default='wrong_answer')
    runtime_ms = db.Column(db.Integer, nullable=True)
    submitted_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', backref='submissions', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'problem_id': self.problem_id,
            'language': self.language,
            'status': self.status,
            'runtime_ms': self.runtime_ms,
            'submitted_at': self.submitted_at.replace(tzinfo=timezone.utc).isoformat(),
        }

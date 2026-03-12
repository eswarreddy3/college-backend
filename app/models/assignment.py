from datetime import datetime, timezone
from app.extensions import db


class AssignmentQuestion(db.Model):
    __tablename__ = 'assignment_questions'

    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.String(100), nullable=False, index=True)  # e.g. 'python-basics'
    topic = db.Column(db.String(100), nullable=False)
    subtopic = db.Column(db.String(100), nullable=False)
    question = db.Column(db.Text, nullable=False)
    options = db.Column(db.JSON, nullable=False)            # list of 4 strings
    correct_answer = db.Column(db.Integer, nullable=False)  # 0-indexed
    explanation = db.Column(db.Text, nullable=True)
    difficulty = db.Column(db.Enum('Easy', 'Medium', 'Hard'), default='Medium')
    points = db.Column(db.Integer, default=5)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self, include_answer=False):
        d = {
            'id': self.id,
            'module_id': self.module_id,
            'topic': self.topic,
            'subtopic': self.subtopic,
            'question': self.question,
            'options': self.options,
            'difficulty': self.difficulty,
            'points': self.points,
            'explanation': self.explanation,
        }
        if include_answer:
            d['correct_answer'] = self.correct_answer
        return d


class AssignmentAttempt(db.Model):
    __tablename__ = 'assignment_attempts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    module_id = db.Column(db.String(100), nullable=False, index=True)
    score = db.Column(db.Integer, default=0)           # points earned
    total_questions = db.Column(db.Integer, default=0)
    correct_count = db.Column(db.Integer, default=0)
    answers = db.Column(db.JSON, nullable=True)        # {str(question_id): selected_index}
    completed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', backref='assignment_attempts', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'module_id': self.module_id,
            'score': self.score,
            'total_questions': self.total_questions,
            'correct_count': self.correct_count,
            'completed_at': self.completed_at.replace(tzinfo=timezone.utc).isoformat(),
        }

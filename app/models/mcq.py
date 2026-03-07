from datetime import datetime, timezone
from app.extensions import db


class MCQQuestion(db.Model):
    __tablename__ = 'mcq_questions'

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(100), nullable=False)       # e.g. 'Python'
    subtopic = db.Column(db.String(100), nullable=False)    # e.g. 'Data Types'
    question = db.Column(db.Text, nullable=False)
    options = db.Column(db.JSON, nullable=False)            # ["A", "B", "C", "D"]
    correct_answer = db.Column(db.Integer, nullable=False)  # 0-indexed
    explanation = db.Column(db.Text, nullable=True)
    difficulty = db.Column(db.Enum('Easy', 'Medium', 'Hard'), default='Medium')
    points = db.Column(db.Integer, default=10)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    attempts = db.relationship('MCQAttempt', backref='question', lazy=True)

    def to_dict(self, include_answer=False):
        d = {
            'id': self.id,
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


class MCQAttempt(db.Model):
    __tablename__ = 'mcq_attempts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('mcq_questions.id'), nullable=False)
    selected_answer = db.Column(db.Integer, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    points_earned = db.Column(db.Integer, default=0)
    attempted_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', backref='mcq_attempts', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'question_id': self.question_id,
            'selected_answer': self.selected_answer,
            'is_correct': self.is_correct,
            'points_earned': self.points_earned,
            'attempted_at': self.attempted_at.isoformat(),
        }

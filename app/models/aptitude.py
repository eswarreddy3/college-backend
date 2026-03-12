from datetime import datetime, timezone
from app.extensions import db


class AptitudeQuestion(db.Model):
    __tablename__ = 'aptitude_questions'

    id = db.Column(db.Integer, primary_key=True)
    topic_name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(500), nullable=False)
    option_b = db.Column(db.String(500), nullable=False)
    option_c = db.Column(db.String(500), nullable=False)
    option_d = db.Column(db.String(500), nullable=False)
    correct_answer = db.Column(db.Enum('A', 'B', 'C', 'D'), nullable=False)
    explanation = db.Column(db.Text, nullable=True)
    points = db.Column(db.Integer, default=10, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self, include_answer=False):
        d = {
            'id': self.id,
            'topic_name': self.topic_name,
            'image_url': self.image_url,
            'question': self.question,
            'option_a': self.option_a,
            'option_b': self.option_b,
            'option_c': self.option_c,
            'option_d': self.option_d,
            'explanation': self.explanation,
            'points': self.points,
        }
        if include_answer:
            d['correct_answer'] = self.correct_answer
        return d


class AptitudeAttempt(db.Model):
    """Tracks correctly answered aptitude questions per user (practice mode)."""
    __tablename__ = 'aptitude_attempts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('aptitude_questions.id'), nullable=False)
    answered_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'question_id', name='uq_apt_attempt_user_question'),
    )

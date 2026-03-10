from datetime import datetime, timezone
from app.extensions import db


class UserStreak(db.Model):
    __tablename__ = 'user_streaks'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    current_streak = db.Column(db.Integer, default=0, nullable=False)
    longest_streak = db.Column(db.Integer, default=0, nullable=False)
    last_activity_date = db.Column(db.Date, nullable=True)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'current_streak': self.current_streak,
            'longest_streak': self.longest_streak,
            'last_activity_date': self.last_activity_date.isoformat() if self.last_activity_date else None,
        }

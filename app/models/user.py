from datetime import datetime, timezone
from app.extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('super_admin', 'college_admin', 'student'), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    first_login = db.Column(db.Boolean, default=True)

    # Student fields
    branch = db.Column(db.String(100), nullable=True)
    section = db.Column(db.String(50), nullable=True)
    roll_number = db.Column(db.String(50), nullable=True)
    passout_year = db.Column(db.Integer, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    linkedin = db.Column(db.String(255), nullable=True)
    github = db.Column(db.String(255), nullable=True)
    password_reset_token = db.Column(db.String(255), nullable=True)
    password_reset_expires = db.Column(db.DateTime, nullable=True)
    resume_data = db.Column(db.JSON, nullable=True)

    points = db.Column(db.Integer, default=0)
    streak = db.Column(db.Integer, default=0)
    last_active = db.Column(db.DateTime, nullable=True)

    # Notification preferences
    email_notifications = db.Column(db.Boolean, default=True)
    assignment_reminders = db.Column(db.Boolean, default=True)
    leaderboard_updates = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    refresh_tokens = db.relationship('RefreshToken', backref='user', lazy=True, cascade='all, delete-orphan')
    activity_logs = db.relationship('ActivityLog', backref='user', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'college_id': self.college_id,
            'college_name': self.college.name if self.college else None,
            'first_login': self.first_login,
            'branch': self.branch,
            'section': self.section,
            'roll_number': self.roll_number,
            'passout_year': self.passout_year,
            'phone': self.phone,
            'linkedin': self.linkedin,
            'github': self.github,
            'points': self.points,
            'streak': self.streak,
            'is_active': self.is_active,
        }

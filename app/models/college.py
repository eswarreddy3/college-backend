from datetime import datetime, timezone
from app.extensions import db


class College(db.Model):
    __tablename__ = 'colleges'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255))
    package_id = db.Column(db.Integer, db.ForeignKey('packages.id'), nullable=True)
    allowed_domain_ids = db.Column(db.JSON, nullable=True)   # None = all domains accessible
    allowed_course_ids = db.Column(db.JSON, nullable=True)   # None = all courses accessible
    is_active = db.Column(db.Boolean, default=True)
    activation_token = db.Column(db.String(255), unique=True, nullable=True)
    activated_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    users = db.relationship('User', backref='college', lazy=True)
    package = db.relationship('Package', backref='colleges', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'package_id': self.package_id,
            'package': self.package.name if self.package else None,
            'plan_type': self.package.plan_type if self.package else None,
            'allowed_domain_ids': self.allowed_domain_ids,
            'allowed_course_ids': self.allowed_course_ids,
            'is_active': self.is_active,
            'activated_at': self.activated_at.replace(tzinfo=timezone.utc).isoformat() if self.activated_at else None,
            'student_count': len([u for u in self.users if u.role == 'student']),
            'created_at': self.created_at.replace(tzinfo=timezone.utc).isoformat(),
        }

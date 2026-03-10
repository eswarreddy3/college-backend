from datetime import datetime, timezone
from app.extensions import db


class Package(db.Model):
    __tablename__ = 'packages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    plan_type = db.Column(db.String(20), nullable=False, default='free')  # free|base|pro|enterprise
    price = db.Column(db.Numeric(10, 2), default=0)  # price per student per year (0 = free/custom)
    features = db.Column(db.JSON, default=list)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'plan_type': self.plan_type,
            'price': float(self.price),
            'features': self.features or [],
            'is_active': self.is_active,
        }

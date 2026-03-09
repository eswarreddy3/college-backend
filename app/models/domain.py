from app.extensions import db


class Domain(db.Model):
    __tablename__ = 'domains'

    id = db.Column(db.String(50), primary_key=True)          # e.g. 'data-science'
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50), default='Database')       # Lucide icon name
    icon_color = db.Column(db.String(50), default='text-blue-400')
    bg_color = db.Column(db.String(50), default='bg-blue-400/20')
    skills = db.Column(db.JSON, default=list)                 # list of skill strings
    is_active = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)

    # relationship: ordered list of domain_courses entries
    domain_courses = db.relationship(
        'DomainCourse', backref='domain', lazy=True,
        order_by='DomainCourse.order_index'
    )

    def total_points(self):
        return sum(
            dc.course.points_per_lesson * dc.course.total_lessons()
            for dc in self.domain_courses
            if dc.course and dc.course.is_active
        )

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'icon': self.icon,
            'icon_color': self.icon_color,
            'bg_color': self.bg_color,
            'skills': self.skills or [],
            'total_points': self.total_points(),
            'total_courses': len([dc for dc in self.domain_courses if dc.course and dc.course.is_active]),
        }


class DomainCourse(db.Model):
    """Junction table: maps courses to domains with ordering."""
    __tablename__ = 'domain_courses'

    id = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.String(50), db.ForeignKey('domains.id'), nullable=False)
    course_id = db.Column(db.String(50), db.ForeignKey('courses.id'), nullable=False)
    order_index = db.Column(db.Integer, default=0)

    course = db.relationship('Course', backref='domain_courses', lazy='joined')

    __table_args__ = (
        db.UniqueConstraint('domain_id', 'course_id', name='uq_domain_course'),
    )

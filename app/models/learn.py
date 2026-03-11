from datetime import datetime, timezone
from app.extensions import db


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.String(50), primary_key=True)          # e.g. 'python'
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)       # 'programming','aptitude','domain'
    difficulty = db.Column(db.String(20), default='Beginner') # Beginner/Intermediate/Advanced
    icon = db.Column(db.String(50), default='Code')           # Lucide icon name
    icon_color = db.Column(db.String(50), default='text-blue-400')
    prerequisite_id = db.Column(db.String(50), db.ForeignKey('courses.id'), nullable=True)
    points_per_lesson = db.Column(db.Integer, default=10)
    is_active = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)

    lessons = db.relationship('Lesson', backref='course', lazy=True,
                               order_by='Lesson.order')

    def total_lessons(self):
        return len([l for l in self.lessons if l.is_active])

    def to_dict(self, lessons_completed=0, is_locked=False, lock_reason=None):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'difficulty': self.difficulty,
            'icon': self.icon,
            'icon_color': self.icon_color,
            'prerequisite_id': self.prerequisite_id,
            'points_per_lesson': self.points_per_lesson,
            'total_lessons': self.total_lessons(),
            'lessons_completed': lessons_completed,
            'is_locked': is_locked,
            'lock_reason': lock_reason,  # 'plan' | 'prerequisite' | None
        }


class Lesson(db.Model):
    __tablename__ = 'lessons'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(50), db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    duration_mins = db.Column(db.Integer, default=10)
    order = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, default=10)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self, is_completed=False):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'title': self.title,
            'duration_mins': self.duration_mins,
            'order': self.order,
            'points': self.points,
            'is_completed': is_completed,
        }


class UserLessonProgress(db.Model):
    __tablename__ = 'user_lesson_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    points_earned = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (db.UniqueConstraint('user_id', 'lesson_id', name='uq_user_lesson'),)

    user = db.relationship('User', backref='lesson_progress', lazy=True)
    lesson = db.relationship('Lesson', backref='progress', lazy=True)

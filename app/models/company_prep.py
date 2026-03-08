from datetime import datetime, timezone
from app.extensions import db


class Company(db.Model):
    __tablename__ = 'companies'

    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(100), nullable=False, unique=True)
    slug           = db.Column(db.String(100), nullable=False, unique=True)
    description    = db.Column(db.Text, nullable=True)
    about_points   = db.Column(db.JSON, default=list)   # bullet-point facts list
    industry       = db.Column(db.String(100), nullable=True)
    founded_year   = db.Column(db.Integer, nullable=True)
    headquarters   = db.Column(db.String(200), nullable=True)
    employee_count = db.Column(db.String(50), nullable=True)   # "600,000+"
    website        = db.Column(db.String(255), nullable=True)
    logo_color     = db.Column(db.String(100), default='from-blue-500 to-blue-700')
    logo_letter    = db.Column(db.String(5), default='?')
    is_active      = db.Column(db.Boolean, default=True)
    created_at     = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    hiring_rounds      = db.relationship('CompanyHiringRound', backref='company', lazy=True,
                                          order_by='CompanyHiringRound.order')
    packages           = db.relationship('CompanyPackage', backref='company', lazy=True)
    aptitude_questions = db.relationship('CompanyAptitudeQuestion', backref='company', lazy=True)
    coding_questions   = db.relationship('CompanyCodingQuestion', backref='company', lazy=True)
    tips               = db.relationship('CompanyTip', backref='company', lazy=True)

    def to_dict(self, include_counts=True):
        d = {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'about_points': self.about_points or [],
            'industry': self.industry,
            'founded_year': self.founded_year,
            'headquarters': self.headquarters,
            'employee_count': self.employee_count,
            'website': self.website,
            'logo_color': self.logo_color,
            'logo_letter': self.logo_letter,
        }
        if include_counts:
            d['aptitude_count'] = len(self.aptitude_questions)
            d['coding_count']   = len(self.coding_questions)
            d['tips_count']     = len(self.tips)
            d['rounds_count']   = len(self.hiring_rounds)
            d['packages_count'] = len(self.packages)
        return d


class CompanyHiringRound(db.Model):
    __tablename__ = 'company_hiring_rounds'

    id             = db.Column(db.Integer, primary_key=True)
    company_id     = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    order          = db.Column(db.Integer, nullable=False)
    name           = db.Column(db.String(100), nullable=False)
    description    = db.Column(db.Text, nullable=True)
    duration       = db.Column(db.String(50), nullable=True)   # "60 minutes"
    is_eliminatory = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'order': self.order,
            'name': self.name,
            'description': self.description,
            'duration': self.duration,
            'is_eliminatory': self.is_eliminatory,
        }


class CompanyPackage(db.Model):
    __tablename__ = 'company_packages'

    id          = db.Column(db.Integer, primary_key=True)
    company_id  = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    role_name   = db.Column(db.String(150), nullable=False)
    type        = db.Column(db.Enum('Full Time', 'Internship'), default='Full Time')
    ctc_min     = db.Column(db.Numeric(6, 2), nullable=True)   # LPA
    ctc_max     = db.Column(db.Numeric(6, 2), nullable=True)
    location    = db.Column(db.String(200), nullable=True)
    eligibility = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'role_name': self.role_name,
            'type': self.type,
            'ctc_min': float(self.ctc_min) if self.ctc_min is not None else None,
            'ctc_max': float(self.ctc_max) if self.ctc_max is not None else None,
            'location': self.location,
            'eligibility': self.eligibility,
        }


class CompanyAptitudeQuestion(db.Model):
    __tablename__ = 'company_aptitude_questions'

    id             = db.Column(db.Integer, primary_key=True)
    company_id     = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    section        = db.Column(db.Enum('Quantitative', 'Logical', 'Verbal', 'Technical'), nullable=False)
    question       = db.Column(db.Text, nullable=False)
    options        = db.Column(db.JSON, nullable=False)      # ["A", "B", "C", "D"]
    correct_answer = db.Column(db.Integer, nullable=False)   # 0-indexed
    explanation    = db.Column(db.Text, nullable=True)
    difficulty     = db.Column(db.Enum('Easy', 'Medium', 'Hard'), default='Medium')
    year           = db.Column(db.Integer, nullable=True)
    is_active      = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'section': self.section,
            'question': self.question,
            'options': self.options,
            'correct_answer': self.correct_answer,
            'explanation': self.explanation,
            'difficulty': self.difficulty,
            'year': self.year,
        }


class CompanyCodingQuestion(db.Model):
    __tablename__ = 'company_coding_questions'

    id            = db.Column(db.Integer, primary_key=True)
    company_id    = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    title         = db.Column(db.String(255), nullable=False)
    description   = db.Column(db.Text, nullable=False)
    difficulty    = db.Column(db.Enum('Easy', 'Medium', 'Hard'), default='Medium')
    tags          = db.Column(db.JSON, default=list)
    solution_hint = db.Column(db.Text, nullable=True)
    year          = db.Column(db.Integer, nullable=True)
    is_active     = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'difficulty': self.difficulty,
            'tags': self.tags or [],
            'solution_hint': self.solution_hint,
            'year': self.year,
        }


class CompanyTip(db.Model):
    __tablename__ = 'company_tips'

    id         = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    category   = db.Column(db.Enum('HR', 'Technical', 'GD', 'Resume'), nullable=False)
    title      = db.Column(db.String(255), nullable=False)
    content    = db.Column(db.Text, nullable=False)
    order      = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'title': self.title,
            'content': self.content,
            'order': self.order,
        }

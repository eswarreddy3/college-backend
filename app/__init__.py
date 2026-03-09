import os
from flask import Flask
from app.extensions import db, migrate, mail, cors
from app.config import config


def create_app(config_name: str = None) -> Flask:
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    cors.init_app(app, resources={r'/api/*': {
        'origins': '*',
        'allow_headers': ['Authorization', 'Content-Type'],
        'methods': ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
    }})

    # Import models so SQLAlchemy knows about them
    with app.app_context():
        from app.models import College, User, Package, RefreshToken, CodingProblem, CodingSubmission, ActivityLog, MCQQuestion, MCQAttempt, Course, Lesson, UserLessonProgress, AssignmentQuestion, AssignmentAttempt, Company, CompanyHiringRound, CompanyPackage, CompanyAptitudeQuestion, CompanyCodingQuestion, CompanyTip, Domain, DomainCourse  # noqa

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.student import student_bp
    from app.routes.admin import admin_bp
    from app.routes.super_admin import super_admin_bp
    from app.routes.coding import coding_bp
    from app.routes.mcq import mcq_bp
    from app.routes.learn import learn_bp
    from app.routes.assignments import assignments_bp
    from app.routes.company_prep import company_prep_bp
    from app.routes.domain_programs import domain_programs_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(student_bp, url_prefix='/api/student')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(super_admin_bp, url_prefix='/api/super-admin')
    app.register_blueprint(coding_bp, url_prefix='/api/coding')
    app.register_blueprint(mcq_bp, url_prefix='/api/mcq')
    app.register_blueprint(learn_bp, url_prefix='/api/learn')
    app.register_blueprint(assignments_bp, url_prefix='/api/assignments')
    app.register_blueprint(company_prep_bp, url_prefix='/api/company-prep')
    app.register_blueprint(domain_programs_bp, url_prefix='/api/domain-programs')

    # Health check
    @app.get('/api/health')
    def health():
        return {'status': 'ok', 'env': config_name}

    return app

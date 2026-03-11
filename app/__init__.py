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
    cors.init_app(
        app,
        origins='*',
        allow_headers=['Authorization', 'Content-Type'],
        methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
        supports_credentials=False,
    )

    # Import models so SQLAlchemy knows about them
    with app.app_context():
        from app.models import College, User, Package, RefreshToken, CodingProblem, CodingSubmission, ActivityLog, MCQQuestion, MCQAttempt, Course, Lesson, UserLessonProgress, AssignmentQuestion, AssignmentAttempt, Company, CompanyHiringRound, CompanyPackage, CompanyAptitudeQuestion, CompanyCodingQuestion, CompanyTip, Domain, DomainCourse, Post, PostLike, Comment, CommentLike  # noqa
        from app.models.streak import UserStreak  # noqa

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
    from app.routes.feed import feed_bp

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
    app.register_blueprint(feed_bp, url_prefix='/api/feed')

    # Ensure CORS headers are present even on unhandled error responses.
    # Flask's default error handler bypasses after_request hooks, so
    # Flask-CORS never gets a chance to inject the header — browsers then
    # report a CORS error that masks the real 4xx/5xx problem.
    @app.after_request
    def _add_cors_on_error(response):
        response.headers.setdefault('Access-Control-Allow-Origin', '*')
        response.headers.setdefault('Access-Control-Allow-Headers', 'Authorization, Content-Type')
        response.headers.setdefault('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        return response

    @app.errorhandler(Exception)
    def _handle_unhandled(e):
        from flask import jsonify as _jsonify
        import traceback
        app.logger.error(traceback.format_exc())
        response = _jsonify({'error': 'Internal server error', 'detail': str(e)})
        response.status_code = 500
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    # Health check
    @app.get('/api/health')
    def health():
        return {'status': 'ok', 'env': config_name}

    return app

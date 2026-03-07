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
        from app.models import College, User, Package, RefreshToken, CodingProblem, CodingSubmission, ActivityLog, MCQQuestion, MCQAttempt  # noqa

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.student import student_bp
    from app.routes.admin import admin_bp
    from app.routes.super_admin import super_admin_bp
    from app.routes.coding import coding_bp
    from app.routes.mcq import mcq_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(student_bp, url_prefix='/api/student')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(super_admin_bp, url_prefix='/api/super-admin')
    app.register_blueprint(coding_bp, url_prefix='/api/coding')
    app.register_blueprint(mcq_bp, url_prefix='/api/mcq')

    # Health check
    @app.get('/api/health')
    def health():
        return {'status': 'ok', 'env': config_name}

    return app

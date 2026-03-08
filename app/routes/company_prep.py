from flask import Blueprint, request, jsonify, g
from app.models.company_prep import (
    Company, CompanyHiringRound, CompanyPackage,
    CompanyAptitudeQuestion, CompanyCodingQuestion, CompanyTip
)
from app.utils.decorators import jwt_required

company_prep_bp = Blueprint('company_prep', __name__)


@company_prep_bp.get('/companies')
@jwt_required
def list_companies():
    companies = Company.query.filter_by(is_active=True).order_by(Company.name).all()
    return jsonify([c.to_dict(include_counts=True) for c in companies]), 200


@company_prep_bp.get('/companies/<slug>')
@jwt_required
def get_company(slug):
    company = Company.query.filter_by(slug=slug, is_active=True).first_or_404()
    data = company.to_dict(include_counts=False)
    data['hiring_rounds'] = [r.to_dict() for r in company.hiring_rounds]
    data['packages'] = [p.to_dict() for p in company.packages]
    return jsonify(data), 200


@company_prep_bp.get('/companies/<slug>/aptitude')
@jwt_required
def get_aptitude(slug):
    company = Company.query.filter_by(slug=slug, is_active=True).first_or_404()
    query = CompanyAptitudeQuestion.query.filter_by(company_id=company.id, is_active=True)
    section = request.args.get('section')
    if section:
        query = query.filter_by(section=section)
    questions = query.order_by(CompanyAptitudeQuestion.section, CompanyAptitudeQuestion.id).all()
    return jsonify([q.to_dict() for q in questions]), 200


@company_prep_bp.get('/companies/<slug>/coding')
@jwt_required
def get_coding(slug):
    company = Company.query.filter_by(slug=slug, is_active=True).first_or_404()
    query = CompanyCodingQuestion.query.filter_by(company_id=company.id, is_active=True)
    difficulty = request.args.get('difficulty')
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    questions = query.order_by(CompanyCodingQuestion.difficulty, CompanyCodingQuestion.id).all()
    return jsonify([q.to_dict() for q in questions]), 200


@company_prep_bp.get('/companies/<slug>/tips')
@jwt_required
def get_tips(slug):
    company = Company.query.filter_by(slug=slug, is_active=True).first_or_404()
    tips = CompanyTip.query.filter_by(company_id=company.id).order_by(
        CompanyTip.category, CompanyTip.order
    ).all()
    grouped: dict = {}
    for tip in tips:
        grouped.setdefault(tip.category, []).append(tip.to_dict())
    return jsonify(grouped), 200

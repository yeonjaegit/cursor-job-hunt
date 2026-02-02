"""회사 지원 현황 라우트"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from extensions import db
from models import Company

companies_bp = Blueprint('companies', __name__)


@companies_bp.route('/companies', methods=['GET'])
@jwt_required()
def get_companies():
    try:
        user_id = int(get_jwt_identity())
        status = request.args.get('status')
        query = Company.query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        companies = query.order_by(Company.applied_date.desc()).all()
        return jsonify({'companies': [c.to_dict() for c in companies]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@companies_bp.route('/companies', methods=['POST'])
@jwt_required()
def create_company():
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        interview_date = None
        if data.get('interview_date'):
            interview_date = datetime.strptime(data['interview_date'], '%Y-%m-%d').date()
        company = Company(
            user_id=user_id,
            name=data['name'],
            position=data['position'],
            status=data.get('status', 'applied'),
            applied_date=datetime.strptime(data['applied_date'], '%Y-%m-%d').date(),
            interview_date=interview_date,
            memo=data.get('memo')
        )
        db.session.add(company)
        db.session.commit()
        return jsonify({'message': '회사가 추가되었습니다', 'company': company.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@companies_bp.route('/companies/<int:company_id>', methods=['PUT'])
@jwt_required()
def update_company(company_id):
    try:
        user_id = int(get_jwt_identity())
        company = Company.query.filter_by(id=company_id, user_id=user_id).first()
        if not company:
            return jsonify({'error': '회사를 찾을 수 없습니다'}), 404
        data = request.get_json()
        if 'name' in data:
            company.name = data['name']
        if 'position' in data:
            company.position = data['position']
        if 'status' in data:
            company.status = data['status']
        if 'applied_date' in data:
            company.applied_date = datetime.strptime(data['applied_date'], '%Y-%m-%d').date()
        if 'interview_date' in data:
            company.interview_date = datetime.strptime(data['interview_date'], '%Y-%m-%d').date() if data['interview_date'] else None
        if 'memo' in data:
            company.memo = data['memo']
        company.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({'message': '회사 정보가 수정되었습니다', 'company': company.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@companies_bp.route('/companies/<int:company_id>', methods=['DELETE'])
@jwt_required()
def delete_company(company_id):
    try:
        user_id = int(get_jwt_identity())
        company = Company.query.filter_by(id=company_id, user_id=user_id).first()
        if not company:
            return jsonify({'error': '회사를 찾을 수 없습니다'}), 404
        db.session.delete(company)
        db.session.commit()
        return jsonify({'message': '회사가 삭제되었습니다'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@companies_bp.route('/companies/stats', methods=['GET'])
@jwt_required()
def get_company_stats():
    try:
        user_id = int(get_jwt_identity())
        total = Company.query.filter_by(user_id=user_id).count()
        by_status = {s: Company.query.filter_by(user_id=user_id, status=s).count()
                     for s in ['applied', 'docs_passed', 'interviewed', 'accepted', 'rejected']}
        return jsonify({'total': total, 'by_status': by_status}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

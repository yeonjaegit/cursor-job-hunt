"""코딩 테스트 라우트"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from extensions import db
from models import CodingProblem

coding_bp = Blueprint('coding', __name__)


@coding_bp.route('/coding', methods=['GET'])
@jwt_required()
def get_coding_problems():
    try:
        user_id = int(get_jwt_identity())
        level = request.args.get('level', type=int)
        query = CodingProblem.query.filter_by(user_id=user_id)
        if level:
            query = query.filter_by(level=level)
        problems = query.order_by(CodingProblem.solved_date.desc()).all()
        return jsonify({'problems': [p.to_dict() for p in problems]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@coding_bp.route('/coding', methods=['POST'])
@jwt_required()
def create_coding_problem():
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        problem = CodingProblem(
            user_id=user_id,
            title=data['title'],
            level=data['level'],
            platform=data.get('platform', '프로그래머스'),
            status=data.get('status', 'solved'),
            solved_date=datetime.strptime(data['solved_date'], '%Y-%m-%d').date(),
            memo=data.get('memo')
        )
        db.session.add(problem)
        db.session.commit()
        return jsonify({'message': '문제가 추가되었습니다', 'problem': problem.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@coding_bp.route('/coding/<int:problem_id>', methods=['PUT'])
@jwt_required()
def update_coding_problem(problem_id):
    try:
        user_id = int(get_jwt_identity())
        problem = CodingProblem.query.filter_by(id=problem_id, user_id=user_id).first()
        if not problem:
            return jsonify({'error': '문제를 찾을 수 없습니다'}), 404
        data = request.get_json()
        if 'title' in data:
            problem.title = data['title']
        if 'level' in data:
            problem.level = data['level']
        if 'platform' in data:
            problem.platform = data['platform']
        if 'status' in data:
            problem.status = data['status']
        if 'solved_date' in data:
            problem.solved_date = datetime.strptime(data['solved_date'], '%Y-%m-%d').date()
        if 'memo' in data:
            problem.memo = data['memo']
        problem.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({'message': '문제 정보가 수정되었습니다', 'problem': problem.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@coding_bp.route('/coding/<int:problem_id>', methods=['DELETE'])
@jwt_required()
def delete_coding_problem(problem_id):
    try:
        user_id = int(get_jwt_identity())
        problem = CodingProblem.query.filter_by(id=problem_id, user_id=user_id).first()
        if not problem:
            return jsonify({'error': '문제를 찾을 수 없습니다'}), 404
        db.session.delete(problem)
        db.session.commit()
        return jsonify({'message': '문제가 삭제되었습니다'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@coding_bp.route('/coding/stats', methods=['GET'])
@jwt_required()
def get_coding_stats():
    try:
        user_id = int(get_jwt_identity())
        total = CodingProblem.query.filter_by(user_id=user_id).count()
        solved = CodingProblem.query.filter_by(user_id=user_id, status='solved').count()
        unsolved = total - solved
        level1 = CodingProblem.query.filter_by(user_id=user_id, level=1, status='solved').count()
        level2 = CodingProblem.query.filter_by(user_id=user_id, level=2, status='solved').count()
        level3_plus = CodingProblem.query.filter(
            CodingProblem.user_id == user_id,
            CodingProblem.level >= 3,
            CodingProblem.status == 'solved'
        ).count()
        return jsonify({
            'total': total, 'solved': solved, 'unsolved': unsolved,
            'level1': level1, 'level2': level2, 'level3_plus': level3_plus
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

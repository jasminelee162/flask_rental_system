from flask import Blueprint, request, jsonify, render_template, url_for
from models import db, House, User
from flask_login import current_user, login_required
from datetime import datetime, timedelta

contract_bp = Blueprint('contract', __name__)


@contract_bp.route('/contract/<int:house_id>/<int:user_id>')
@login_required
def show_contract(house_id, user_id):
    user = User.query.get(user_id)
    house = House.query.get(house_id)

    if not all([user, house]):
        return "用户或房源不存在", 404

    return render_template(
        'contract_confirmation.html',
        house=house,
        user=user,
        current_user=current_user,
        now=datetime.now(),
        timedelta=timedelta
    )


@contract_bp.route('/api/contract/data')
def check_rental_status():
    try:
        house_id = request.args.get('house_id')
        if not house_id:
            return jsonify({'success': False, 'message': '缺少房源ID'}), 400

        house = House.query.get(house_id)
        if not house:
            return jsonify({'success': False, 'message': '房源不存在'}), 404

        return jsonify({
            'success': True,
            'data': {
                'is_rented': house.rental_status == 'rented',
                'house_info': {
                    'title': house.title,
                    'address': f"{house.region}{house.block}{house.address}",
                    'price': house.price
                }
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@contract_bp.route('/api/sign', methods=['POST'])
@login_required
def sign_contract():
    try:
        data = request.get_json()

        if not data or 'house_id' not in data:
            return jsonify({'success': False, 'message': '缺少必要字段'}), 400

        house = House.query.get(data['house_id'])
        if not house:
            return jsonify({'success': False, 'message': '房源不存在'}), 404

        house.rental_status = '已出租'
        current_user.rent_id = house.id
        db.session.commit()

        return jsonify({
            'success': True,
            'message': '合同签署成功',
            'house_id': house.id
        })
    except Exception as e:
        db.session.rollback()
        print(f"数据库操作失败: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500
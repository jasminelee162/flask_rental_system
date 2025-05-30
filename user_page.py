from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from models import User, House, db
from flask_login import login_required, current_user

user_page = Blueprint('user_page', __name__)

@user_page.route('/become-landlord', methods=['POST'])
@login_required
def become_landlord():
    try:
        # 获取当前用户
        user = User.query.get(current_user.id)
        if not user:
            return jsonify({'success': False, 'message': '用户不存在'})
        
        # 如果已经是房东，直接返回成功
        if user.is_landlord:
            return jsonify({'success': True, 'message': '您已经是房东了'})
        
        # 更新用户为房东
        user.is_landlord = True
        db.session.commit()
        
        return jsonify({'success': True, 'message': '恭喜您成为房东！'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'操作失败：{str(e)}'}) 
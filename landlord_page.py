from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db, House
from datetime import datetime
import os
from werkzeug.utils import secure_filename

landlord_page = Blueprint('landlord_page', __name__)

def check_landlord():
    """检查当前用户是否是房东"""
    print(f"检查房东权限: is_authenticated={current_user.is_authenticated}, is_landlord={current_user.is_landlord}")
    if not current_user.is_authenticated or not current_user.is_landlord:
        flash('您没有房东权限!', 'error')
        return False
    return True

@landlord_page.route('/my/houses')
@login_required
def my_houses():
    """房东查看自己的房源列表"""
    print(f"访问我的房源: is_authenticated={current_user.is_authenticated}, is_landlord={current_user.is_landlord}")
    if not check_landlord():
        return redirect(url_for('index_page.index'))
        
    houses = House.query.filter_by(landlord_id=current_user.id).all()
    return render_template('landlord/house_list.html', houses=houses)

@landlord_page.route('/house/add', methods=['GET', 'POST'])
@login_required
def add_house():
    """房东添加房源"""
    if not check_landlord():
        return redirect(url_for('index_page.index'))
        
    if request.method == 'POST':
        house = House(
            title=request.form.get('title'),
            rooms=request.form.get('rooms'),
            area=request.form.get('area'),
            price=request.form.get('price'),
            direction=request.form.get('direction'),
            rent_type=request.form.get('rent_type'),
            region=request.form.get('region'),
            block=request.form.get('block'),
            address=request.form.get('address'),
            traffic=request.form.get('traffic'),
            sheshi=request.form.get('sheshi'),
            phone_num=current_user.phone_num,
            landlord_id=current_user.id,
            publish_time=int(datetime.now().timestamp()),
            page_view=0
        )
        
        # 处理图片上传
        if 'picture' in request.files:
            file = request.files['picture']
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join('static/img', filename))
                house.picture = filename
        
        try:
            db.session.add(house)
            db.session.commit()
            flash('房源添加成功!', 'success')
            return redirect(url_for('landlord_page.my_houses'))
        except Exception as e:
            db.session.rollback()
            flash('添加失败,请重试!', 'error')
            
    return render_template('landlord/house_add.html')

@landlord_page.route('/house/edit/<int:house_id>', methods=['GET', 'POST'])
@login_required
def edit_house(house_id):
    """房东编辑房源"""
    if not check_landlord():
        return redirect(url_for('index_page.index'))
        
    house = House.query.get_or_404(house_id)
    
    # 验证是否是房源的所有者
    if house.landlord_id != current_user.id:
        flash('您没有权限编辑该房源!', 'error')
        return redirect(url_for('landlord_page.my_houses'))
    
    if request.method == 'POST':
        house.title = request.form.get('title')
        house.rooms = request.form.get('rooms')
        house.area = request.form.get('area')
        house.price = request.form.get('price')
        house.direction = request.form.get('direction')
        house.rent_type = request.form.get('rent_type')
        house.region = request.form.get('region')
        house.block = request.form.get('block')
        house.address = request.form.get('address')
        house.traffic = request.form.get('traffic')
        house.sheshi = request.form.get('sheshi')
        
        # 处理图片更新
        if 'picture' in request.files:
            file = request.files['picture']
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join('static/img', filename))
                house.picture = filename
        
        try:
            db.session.commit()
            flash('房源信息更新成功!', 'success')
            return redirect(url_for('landlord_page.my_houses'))
        except Exception as e:
            db.session.rollback()
            flash('更新失败,请重试!', 'error')
            
    return render_template('landlord/house_edit.html', house=house)

@landlord_page.route('/house/delete/<int:house_id>')
@login_required
def delete_house(house_id):
    """房东删除房源"""
    if not check_landlord():
        return redirect(url_for('index_page.index'))
        
    house = House.query.get_or_404(house_id)
    
    # 验证是否是房源的所有者
    if house.landlord_id != current_user.id:
        flash('您没有权限删除该房源!', 'error')
        return redirect(url_for('landlord_page.my_houses'))
    
    try:
        db.session.delete(house)
        db.session.commit()
        flash('房源删除成功!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('删除失败,请重试!', 'error')
        
    return redirect(url_for('landlord_page.my_houses')) 
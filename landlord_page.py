from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, jsonify
from flask_login import login_required, current_user
from models import db, House
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from flask_caching import Cache

landlord_page = Blueprint('landlord_page', __name__)
cache = Cache()

def check_landlord():
    """检查当前用户是否是房东"""
    if not current_user.is_authenticated or not current_user.is_landlord:
        flash('您没有房东权限!', 'error')
        return False
    return True

@landlord_page.route('/my/houses')
@login_required
def my_houses():
    """房东查看自己的房源列表"""
    if not check_landlord():
        return redirect(url_for('index_page.index'))
    
    # 获取分页参数
    page = request.args.get('page', 1, type=int)
    per_page = 9  # 每页显示9个房源
    
    # 打印调试信息
    print(f"当前用户ID: {current_user.id}")
    print(f"当前用户是否是房东: {current_user.is_landlord}")
    
    # 直接从数据库获取当前房东的房源
    query = House.query.filter_by(landlord_id=current_user.id)\
        .order_by(House.publish_time.desc())
    
    # 打印SQL查询语句
    print(f"SQL查询: {query}")
    
    houses = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # 打印查询结果
    print(f"查询到的房源数量: {houses.total}")
    for house in houses.items:
        print(f"房源ID: {house.id}, 房东ID: {house.landlord_id}, 标题: {house.title}")
    
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
                # 生成缩略图
                from PIL import Image
                img = Image.open(file)
                img.thumbnail((800, 600))  # 限制图片大小
                img.save(os.path.join('static/img', filename), optimize=True, quality=85)
                house.picture = filename
        
        try:
            db.session.add(house)
            db.session.commit()
            # 清除缓存
            cache.delete_memoized(my_houses)
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

@landlord_page.route('/house/delete/<int:house_id>', methods=['POST'])
@login_required
def delete_house(house_id):
    """房东删除房源"""
    if not check_landlord():
        return jsonify({'success': False, 'message': '您没有房东权限!'})
        
    house = House.query.get_or_404(house_id)
    
    # 验证是否是房源的所有者
    if house.landlord_id != current_user.id:
        return jsonify({'success': False, 'message': '您没有权限删除该房源!'})
    
    try:
        # 删除房源图片
        if house.picture:
            try:
                os.remove(os.path.join('static/img', house.picture))
            except OSError:
                pass  # 忽略文件删除错误
        
        db.session.delete(house)
        db.session.commit()
        # 清除缓存
        cache.delete_memoized(my_houses)
        return jsonify({'success': True, 'message': '房源删除成功!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': '删除失败,请重试!'}) 
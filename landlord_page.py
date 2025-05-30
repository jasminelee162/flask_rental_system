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
    
    # 使用缓存获取房源列表
    cache_key = f'landlord_houses_{current_user.id}_page_{page}'
    houses_data = cache.get(cache_key)
    
    if houses_data is None:
        # 如果缓存中没有，从数据库获取
        query = House.query.filter_by(landlord_id=current_user.id)\
            .order_by(House.publish_time.desc())
        houses = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # 缓存查询结果
        houses_data = {
            'items': [{
                'id': house.id,
                'title': house.title,
                'rooms': house.rooms,
                'area': house.area,
                'price': house.price,
                'direction': house.direction,
                'rent_type': house.rent_type,
                'region': house.region,
                'block': house.block,
                'address': house.address,
                'traffic': house.traffic,
                'sheshi': house.sheshi,
                'picture': house.picture,
                'publish_time': house.publish_time,
                'page_view': house.page_view
            } for house in houses.items],
            'total': houses.total,
            'pages': houses.pages,
            'page': houses.page,
            'has_prev': houses.has_prev,
            'has_next': houses.has_next,
            'prev_num': houses.prev_num,
            'next_num': houses.next_num
        }
        # 设置缓存，有效期5分钟
        cache.set(cache_key, houses_data, timeout=300)
    
    # 创建分页对象
    class SimplePagination:
        def __init__(self, items, page, per_page, total, pages):
            self.items = items
            self.page = page
            self.per_page = per_page
            self.total = total
            self.pages = pages
            self.has_prev = page > 1
            self.has_next = page < pages
            self.prev_num = page - 1 if page > 1 else None
            self.next_num = page + 1 if page < pages else None
            
        def iter_pages(self, left_edge=2, left_current=2, right_current=3, right_edge=2):
            last = 0
            for num in range(1, self.pages + 1):
                if (num <= left_edge or
                    (num > self.page - left_current - 1 and
                     num < self.page + right_current) or
                    num > self.pages - right_edge + 1):
                    if last + 1 != num:
                        yield None
                    yield num
                    last = num
    
    # 从缓存数据创建房源对象列表
    houses_items = []
    for item in houses_data['items']:
        house = House()
        for key, value in item.items():
            setattr(house, key, value)
        houses_items.append(house)
    
    # 创建分页对象
    houses = SimplePagination(
        items=houses_items,
        page=houses_data['page'],
        per_page=per_page,
        total=houses_data['total'],
        pages=houses_data['pages']
    )
    
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
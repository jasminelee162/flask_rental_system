from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db, House, User
from datetime import datetime

agent_page = Blueprint('agent_page', __name__)

# 房东列表页面
@agent_page.route('/agent/list')
@login_required
def agent_list():
    """查看房东列表"""
    if not current_user.is_landlord:
        flash('您没有权限访问此页面!', 'error')
        return redirect(url_for('index_page.index'))
        
    landlords = User.query.filter_by(is_landlord=True).all()
    return render_template('agent_list.html', landlords=landlords)

# 添加房东
@agent_page.route('/agent/add', methods=['GET', 'POST'])
def add_agent():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        company = request.form.get('company')
        
        if not all([name, phone]):
            flash('姓名和电话为必填项!', 'error')
            return redirect(url_for('agent_page.add_agent'))
            
        agent = User(
            name=name,
            phone=phone,
            email=email,
            address=address,
            company=company
        )
        
        try:
            db.session.add(agent)
            db.session.commit()
            flash('房东添加成功!', 'success')
            return redirect(url_for('agent_page.agent_list'))
        except Exception as e:
            db.session.rollback()
            flash('添加失败,请重试!', 'error')
            return redirect(url_for('agent_page.add_agent'))
            
    return render_template('agent_add.html')

# 编辑房东信息
@agent_page.route('/agent/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_agent(id):
    """编辑房东信息"""
    if not current_user.is_landlord:
        flash('您没有权限访问此页面!', 'error')
        return redirect(url_for('index_page.index'))
        
    landlord = User.query.get_or_404(id)
    if not landlord.is_landlord:
        flash('该用户不是房东!', 'error')
        return redirect(url_for('agent_page.agent_list'))
    
    if request.method == 'POST':
        landlord.name = request.form.get('name')
        landlord.email = request.form.get('email')
        landlord.addr = request.form.get('address')
        
        try:
            db.session.commit()
            flash('房东信息更新成功!', 'success')
            return redirect(url_for('agent_page.agent_list'))
        except Exception as e:
            db.session.rollback()
            flash('更新失败,请重试!', 'error')
            
    return render_template('agent_edit.html', landlord=landlord)

# 删除房东
@agent_page.route('/agent/delete/<int:id>')
def delete_agent(id):
    agent = User.query.get_or_404(id)
    
    try:
        db.session.delete(agent)
        db.session.commit()
        flash('房东删除成功!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('删除失败,请重试!', 'error')
        
    return redirect(url_for('agent_page.agent_list'))

# 房东的房源列表
@agent_page.route('/agent/<int:id>')
@login_required
def agent_detail(id):
    """查看房东详情"""
    if not current_user.is_landlord:
        flash('您没有权限访问此页面!', 'error')
        return redirect(url_for('index_page.index'))
        
    landlord = User.query.get_or_404(id)
    if not landlord.is_landlord:
        flash('该用户不是房东!', 'error')
        return redirect(url_for('agent_page.agent_list'))
        
    houses = House.query.filter_by(landlord_id=landlord.id).all()
    return render_template('agent_detail.html', landlord=landlord, houses=houses)

# 房东添加房源
@agent_page.route('/agent/house/add/<int:agent_id>', methods=['GET', 'POST'])
def add_house(agent_id):
    agent = User.query.get_or_404(agent_id)
    
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
            phone_num=agent.phone,
            landlord_id=agent_id,
            landlord_name=agent.name,
            landlord_phone=agent.phone,
            publish_time=int(datetime.now().timestamp()),
            page_view=0
        )
        
        # 处理图片上传
        if 'picture' in request.files:
            file = request.files['picture']
            if file:
                # 保存图片文件
                filename = secure_filename(file.filename)
                file.save(os.path.join('static/img', filename))
                house.picture = filename
        
        try:
            db.session.add(house)
            db.session.commit()
            flash('房源添加成功!', 'success')
            return redirect(url_for('agent_page.agent_detail', id=agent_id))
        except Exception as e:
            db.session.rollback()
            flash('添加失败,请重试!', 'error')
            
    return render_template('house_add.html', agent=agent)

# 房东编辑房源
@agent_page.route('/agent/house/edit/<int:house_id>', methods=['GET', 'POST'])
def edit_house(house_id):
    house = House.query.get_or_404(house_id)
    
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
            return redirect(url_for('agent_page.agent_detail', id=house.landlord_id))
        except Exception as e:
            db.session.rollback()
            flash('更新失败,请重试!', 'error')
            
    return render_template('house_edit.html', house=house)

# 房东删除房源
@agent_page.route('/agent/house/delete/<int:house_id>')
def delete_house(house_id):
    house = House.query.get_or_404(house_id)
    agent_id = house.landlord_id
    
    try:
        db.session.delete(house)
        db.session.commit()
        flash('房源删除成功!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('删除失败,请重试!', 'error')
        
    return redirect(url_for('agent_page.agent_detail', id=agent_id)) 
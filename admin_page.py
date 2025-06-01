from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import House, User, Tuijian
from datetime import datetime
from utils.connect_to_database import query_data
from settings import db
from sqlalchemy import func
from utils.regression_data import linear_model_main
from utils.pearson_tuijian import recommed
from datetime import date
from flask import session, redirect, url_for, render_template
from models import UserLoginLog
from sqlalchemy import func
from flask import Blueprint, render_template

admin_page = Blueprint('admin_page', __name__, template_folder='templates')


@admin_page.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == '123':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_page.dashboard'))
        else:
            flash('账号或密码错误', 'danger')

    return render_template('admin_login.html')


# 后台首页
@admin_page.route('/admin/dashboard')
def dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_page.admin_login'))

    today = date.today()
    # 查询当天活跃用户数量，去重统计
    active_user_count = db.session.query(func.count(UserLoginLog.user_id.distinct())) \
                                  .filter(UserLoginLog.login_date == today) \
                                  .scalar()

    return render_template('admin_dashboard.html', active_user_count=active_user_count)



@admin_page.route('/admin/properties')
def admin_properties():
    # 获取当前页码，默认第1页
    page_num = request.args.get('page', 1, type=int)

    # 限制页码范围
    if page_num < 1:
        page_num = 1

    # 每页显示10条
    per_page = 10

    # 分页查询（不按时间排序，按id升序排序）
    pagination = House.query.order_by(House.id.asc()).paginate(page=page_num, per_page=per_page)
    house_list = pagination.items

    # 如果你模板需要publish_time作为datetime对象，这里可以保留，不需要的话可以注释掉
    # for house in house_list:
    #     if isinstance(house.publish_time, int):
    #         house.publish_time = datetime.fromtimestamp(house.publish_time)

    # 生成页码范围，最多显示10页（或者实际总页数）
    total_pages = pagination.pages
    max_pages = min(total_pages, 10)
    page_range = range(1, max_pages + 1)

    return render_template('admin_properties.html',
                           house_list=house_list,
                           page_num=page_num,
                           page_range=page_range,
                           total_pages=total_pages)





@admin_page.route('/admin/messages')
def messages():
    return render_template('admin_messages.html')  # 暂未实现

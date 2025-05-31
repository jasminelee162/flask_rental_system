from flask import Blueprint, render_template, jsonify, request
from models import House, User, Tuijian
from datetime import datetime
from utils.connect_to_database import query_data
from settings import db
from sqlalchemy import func
from utils.regression_data import linear_model_main
from utils.pearson_tuijian import recommed
# admin_page.py

from flask import Blueprint, render_template

admin_page = Blueprint('admin_page', __name__, template_folder='templates')

@admin_page.route('/admin')
def dashboard():
    return render_template('admin_dashboard.html')



@admin_page.route('/admin/properties')
def admin_properties():
    # 获取当前页码，默认第1页
    page_num = request.args.get('page', 1, type=int)

    # 限制页码范围
    if page_num < 1:
        page_num = 1

    # 每页显示10条
    per_page = 10

    # 分页查询
    pagination = House.query.order_by(House.publish_time.desc()).paginate(page=page_num, per_page=per_page)
    house_list = pagination.items

    # 转换时间戳为 datetime 对象，方便模板使用 strftime
    for house in house_list:
        if isinstance(house.publish_time, int):
            house.publish_time = datetime.fromtimestamp(house.publish_time)

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

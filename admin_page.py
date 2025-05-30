from flask import Blueprint, render_template, jsonify, request
from models import House, User, Tuijian
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
def properties():
    return render_template('admin_properties.html')

@admin_page.route('/admin/messages')
def messages():
    return render_template('admin_messages.html')  # 暂未实现

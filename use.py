import random
import string
from captcha.image import ImageCaptcha
from flask import Blueprint, request, Response, jsonify, render_template, redirect, session, send_file, url_for
from models import User, House
from settings import db
from flask_login import login_user, logout_user, login_required, current_user
import json
import random
import string
from captcha.image import ImageCaptcha

user_page = Blueprint('user_page', __name__)

# 实现注册功能
"""
1. 创建一个视图函数 /register POST请求方式
2. 获取用户的注册信息 昵称 密码 邮箱
3. 校验用户昵称是否已经存在
    3.1 昵称已经存在了 ==> 用户已经注册过这个用户名了 ==> 返回提示信息 告诉用户这个名字 你不能使用
    3.2 昵称不存在    ==> 用户名为使用过           ==> 保存用户信息  然后跳转到用户中心页 再设置cookie
"""


@user_page.route('/register', methods=["POST"])
def register():
    # 获取注册信息（新增is_landlord参数）
    name = request.form['username']
    password = request.form['password']
    email = request.form['email']
    is_landlord = request.form.get('is_landlord') == '1'  # 转换为布尔值

    # 校验用户名是否存在
    user_exists = User.query.filter(User.name == name).first()
    if user_exists:
        return jsonify({'valid': '0', 'msg': '用户名已存在！'})

    # 创建用户对象（新增is_landlord字段）
    new_user = User(
        name=name,
        password=password,
        email=email,
        is_landlord=is_landlord  # 使用布尔值
    )
    db.session.add(new_user)
    db.session.commit()

    # 构造响应
    res = Response(json.dumps({'valid': '1', 'msg': '注册成功', 'is_landlord': '1' if is_landlord else '0'}))
    res.set_cookie('name', name, 3600 * 2)
    res.set_cookie('userId', str(user.id))  # 确保 user.id 是 int
    res.set_cookie('is_landlord', '1' if is_landlord else '0', 3600 * 2)  # 存储为字符串
    return res


# ================== 用户中心页修改 ==================
@user_page.route('/<name>')
def user(name):
    # 查询用户表  获取用户对象
    # first 获取结果的时候 如果有结果  就返回第一个结果 如果没有结果 就直接返回None
    # all   获取结果的时候 如果有结果  返回符合条件的所有结果 放在一个列表中  如果没有结果 就直接返回空列表
    user = User.query.filter(User.name == name).first()

    # 校验用户身份和Cookie
    if not user or user.name != request.cookies.get('name'):
        return redirect('/')

    # 解析收藏和浏览记录（保持原有逻辑）
    collect_house_list, seen_house_list = [], []
    for field, lst in [('collect_id', collect_house_list), ('seen_id', seen_house_list)]:
        ids = getattr(user, field)
        if ids:
            for hid in ids.split(','):
                house = House.query.get(int(hid))
                if house:
                    lst.append(house)

    # 传递房东标识到模板
    return render_template(
        'user_page.html',
        user=user,
        collect_house_list=collect_house_list,
        seen_house_list=seen_house_list,
        is_landlord=user.is_landlord  # 传递房东状态
    )


# ================== 登录功能修改 ==================
@user_page.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
        
    # 获取用户提交的信息，使用 get() 方法安全地获取表单数据
    name = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    captcha_input = request.form.get('captcha', '').strip()

    # 验证表单数据是否完整
    if not name or not password:
        return jsonify({'valid': '0', 'msg': '用户名和密码不能为空！'})

    # 验证码校验
    if captcha_input.upper() != session.get('captcha_code', '').upper():
        return jsonify({'valid': '0', 'msg': '验证码错误！'})

    # 查询用户（包含房东标识）
    user = User.query.filter(User.name == name).first()
    if not user:
        return jsonify({'valid': '0', 'msg': '用户名不存在！'})

    if user.password != password:
        return jsonify({'valid': '0', 'msg': '密码错误！'})

    # 使用 flask_login 登录用户
    login_user(user)

    # 打印调试信息
    print(f"用户登录成功: {user.name}, is_landlord: {user.is_landlord}, is_authenticated: {current_user.is_authenticated}")

    # 登录成功后返回房东状态
    res = Response(json.dumps({
        'valid': '1',
        'msg': '登录成功',
        'name': user.name,
        'is_landlord': '1' if user.is_landlord else '0'  # 转换为字符串
    }))
    res.set_cookie('name', user.name, 3600 * 2)
    res.set_cookie('userId', str(user.id))  # 确保 user.id 是 int
    res.set_cookie('is_landlord', '1' if user.is_landlord else '0', 3600 * 2)  # 存储为字符串
    return res



# ================== 修改用户信息功能扩展 ==================
@user_page.route('/modify/userinfo/<option>', methods=['POST'])
def modify_info(option):
    y_name = request.form['y_name']
    user = User.query.filter(User.name == y_name).first()

    if not user:
        return jsonify({'ok': '0', 'msg': '用户不存在'})

    if option == 'is_landlord':  # 新增修改房东身份的选项
        new_is_landlord = request.form['is_landlord']
        user.is_landlord = new_is_landlord
        db.session.commit()
        # 更新Cookie中的房东状态
        res = Response(json.dumps({'ok': '1', 'msg': '身份修改成功'}))
        res.set_cookie('is_landlord', new_is_landlord, 3600 * 2)
        return res

    # 原有字段修改逻辑保持不变
    # ...（其他option的处理代码）

    return jsonify({'ok': '1', 'msg': '修改成功'})


# ================== 辅助功能（保持原有逻辑） ==================
@user_page.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()  # 使用 flask_login 登出用户
    res = Response(json.dumps({'valid': '1', 'msg': '退出成功'}))
    res.delete_cookie('name')
    res.delete_cookie('is_landlord')  # 同时删除房东状态Cookie
    return res


@user_page.route('/captcha')
def get_captcha():
    # 生成4位随机验证码
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    session['captcha_code'] = code  # 存入 session

    image = ImageCaptcha()
    data = image.generate(code)
    return send_file(data, mimetype='image/png')
from flask import Flask
from settings import Config, db
from list_page import list_page
from index_page import index_page
from detail_page import detail_page
from use import user_page
from chat_routes import chat_bp

from agent_page import agent_page
from landlord_page import landlord_page, cache
from admin_page import admin_page
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from models import User
from flask_caching import Cache


app = Flask(__name__)
app.secret_key = 'your_very_secret_key'

app.config.from_object(Config)

# 配置缓存
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

# 初始化 Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_page.login'  # 设置登录视图的端点
login_manager.login_message = '请先登录'  # 设置登录提示消息

@login_manager.user_loader
def load_user(user_id):
    """加载用户的回调函数"""
    return User.query.get(int(user_id))

db.init_app(app)
migrate = Migrate(app, db)  # 初始化 Flask-Migrate
Bootstrap(app)
            # 将蓝图注册到app中
            # app.register_blueprint(index_page, url_prefix='/')
            # app.register_blueprint(list_page, url_prefix='/')
            # app.register_blueprint(detail_page, url_prefix='/')
            # app.register_blueprint(user_page, url_prefix='/')
            # app.register_blueprint(chat_bp)
            # cache.init_app(app)  # 初始化缓存

# 将蓝图注册到app中，为每个蓝图设置不同的 url_prefix
app.register_blueprint(list_page, url_prefix='/list')
app.register_blueprint(detail_page, url_prefix='/')#加上detail好像会报错呢
app.register_blueprint(user_page, url_prefix='/user')
app.register_blueprint(agent_page, url_prefix='/agent')
app.register_blueprint(landlord_page, url_prefix='/landlord')
app.register_blueprint(admin_page, url_prefix='/admin')
app.register_blueprint(index_page)  # 首页蓝图不需要 url_prefix
app.register_blueprint(chat_bp)


if __name__ == '__main__':
    app.run(debug=True)

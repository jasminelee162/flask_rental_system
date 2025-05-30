from settings import db
from flask_login import UserMixin


# soufang 表的模型类
class House(db.Model):
    # 定义表名
    __tablename__ = 'house_info'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    rooms = db.Column(db.String(100))
    area = db.Column(db.String(100))
    price = db.Column(db.String(100))
    direction = db.Column(db.String(100))
    rent_type = db.Column(db.String(100))
    region = db.Column(db.String(100))
    block = db.Column(db.String(100))
    address = db.Column(db.String(100))
    traffic = db.Column(db.String(100))
    publish_time = db.Column(db.Integer)
    sheshi = db.Column(db.TEXT)
    page_view = db.Column(db.Integer)
    phone_num = db.Column(db.String(100))
    picture = db.Column(db.String(255))
    
    # 房东ID(关联用户表)，使用与 user_info.id 相同的类型
    landlord_id = db.Column(db.Integer, db.ForeignKey('user_info.id', ondelete='SET NULL'))

    # 重写__repr__方法， 方便我们查看对象的输出内容
    def __repr__(self):
        return 'House: %s, %s' % (self.address, self.id)


# tuijian表的模型类
class Tuijian(db.Model):
    __tablename__ = 'recommendation'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    house_id = db.Column(db.Integer)
    title = db.Column(db.String(100))
    address = db.Column(db.String(100))
    block = db.Column(db.String(100))
    score = db.Column(db.Integer)
    picture = db.Column(db.String(255))


# userinfo表的模型类
class User(UserMixin, db.Model):
    __tablename__ = 'user_info'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))
    addr = db.Column(db.String(100))
    collect_id = db.Column(db.String(250))
    seen_id = db.Column(db.String(250))
    is_landlord = db.Column(db.Boolean, default=False)  # 是否是房东

    # 与房源的一对多关系
    houses = db.relationship('House', backref='landlord', lazy=True)

    def get_id(self):
        """返回用户ID"""
        return str(self.id)

    def is_active(self):
        """用户是否激活"""
        return True

    def is_authenticated(self):
        """用户是否已认证"""
        return True

    def is_anonymous(self):
        """是否是匿名用户"""
        return False

    # 重写__repr__方法， 方便我们查看对象的输出内容
    def __repr__(self):
        return 'User: %s, %s' % (self.name, self.id)
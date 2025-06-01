from settings import db
from flask_login import UserMixin
from datetime import datetime
from datetime import date


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
    landlord_id = db.Column(db.Integer)
    rental_status = db.Column(db.String(100))

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
    rent_id = db.Column(db.String(250))

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

    @property
    def rented_houses(self):
        """获取用户租赁的所有房源"""
        if not self.rent_id:
            return []
        try:
            house_ids = [int(hid) for hid in self.rent_id.split(',') if hid.strip()]
            return House.query.filter(House.id.in_(house_ids)).all()
        except Exception as e:
            print(f"解析rent_id出错: {str(e)}")
            return []

    def add_rental(self, house_id):
        """添加租赁关系"""
        current_ids = set()
        if self.rent_id:
            current_ids = {hid for hid in self.rent_id.split(',') if hid.strip()}
        current_ids.add(str(house_id))
        self.rent_id = ','.join(current_ids)

    def rented_houses(self):
        """获取用户所有出租的房源"""
        if not self.rent_id:
            return []
        try:
            house_ids = [int(hid) for hid in self.rent_id.split(',') if hid.strip()]
            return House.query.filter(House.id.in_(house_ids)).all()
        except Exception as e:
            print(f"解析rent_id出错: {str(e)}")
            return []


# message_info 表的模型类
class MessageInfo(db.Model):
    __tablename__ = 'message_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 这里要有主键
    userId = db.Column(db.Integer, nullable=False)         # 发送者 user_id
    landlordId = db.Column(db.Integer, nullable=False)     # 接收者 landlord_id，字段名必须和数据库一致
    message = db.Column(db.String(500), nullable=False)    # 消息内容
    user_flag = db.Column(db.Integer, default=0)
    landlord_flag = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Message from {self.userId} to {self.landlordId}: {self.message}>'

# viewing_appointment表的模型块
class Appointment(db.Model):
    __tablename__ = 'viewing_appointment'

    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey('house_info.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.id'))
    landlord_id = db.Column(db.Integer, db.ForeignKey('user_info.id'))
    appointment_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')
    note = db.Column(db.Text)
    # 移除 created_at 字段
    # 添加关系属性
    house = db.relationship('House', backref='appointments')
    user = db.relationship('User', foreign_keys=[user_id])
    landlord = db.relationship('User', foreign_keys=[landlord_id])

class UserLoginLog(db.Model):
    __tablename__ = 'user_login_log'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.id'))
    login_date = db.Column(db.Date, nullable=False)

    __table_args__ = (db.UniqueConstraint('user_id', 'login_date', name='unique_user_login'),)

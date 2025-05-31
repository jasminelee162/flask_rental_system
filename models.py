from settings import db


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
    #liangdian = db.Column(db.TEXT)
    #peitao = db.Column(db.TEXT)
    #chuxing = db.Column(db.TEXT)
    page_view = db.Column(db.Integer)
    #people_name = db.Column(db.String(100))
    phone_num = db.Column(db.String(100))
    #house_num = db.Column(db.String(100))
    picture = db.Column(db.String(255))
    landlord_id = db.Column(db.Integer)

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
class User(db.Model):
    __tablename__ = 'user_info'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))
    addr = db.Column(db.String(100))
    collect_id = db.Column(db.String(250))
    seen_id = db.Column(db.String(250))

    # 重写__repr__方法， 方便我们查看对象的输出内容
    def __repr__(self):
        return 'User: %s, %s' % (self.name, self.id)


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

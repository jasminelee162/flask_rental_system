# chat_routes.py
from flask import Blueprint, request, jsonify
from models import db, MessageInfo, User  # 根据项目实际导入
from flask import render_template

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat/list')
def chat_list():
    user_id = int(request.cookies.get('userId'))
    landlord_id = request.args.get('landlord_id', type=int)
    print(f"chat/list called with user_id={user_id}, landlord_id={landlord_id}")

    records = MessageInfo.query.filter(
        (MessageInfo.userId == user_id) | (MessageInfo.landlordId == user_id)
    ).all()

    user_ids = set()
    for record in records:
        if record.userId == user_id:
            user_ids.add(record.landlordId)
        elif record.landlordId == user_id:
            user_ids.add(record.userId)

    if landlord_id and landlord_id not in user_ids and landlord_id != user_id:
        print(f"Adding landlord_id {landlord_id} to user_ids")
        user_ids.add(landlord_id)

        # ✅ 插入房东自动欢迎消息（仅首次联系）
        existing = MessageInfo.query.filter_by(userId=user_id, landlordId=landlord_id).first()
        if not existing:
            user = User.query.get(user_id)
            username = user.name if user else "用户"

            welcome_msg = f"您好 {username}，请问有什么能够帮您的吗？"
            auto_message = MessageInfo(
                userId=landlord_id,      # 房东发的
                landlordId=user_id,      # 发给用户
                message=welcome_msg,
                user_flag=0,
                landlord_flag=1
            )
            db.session.add(auto_message)
            db.session.commit()
            print("自动欢迎消息已发送")

    users = User.query.filter(User.id.in_(user_ids)).all()
    result = [{'id': u.id, 'name': u.name} for u in users]
    print(f"Returning users: {result}")
    return jsonify(result)




@chat_bp.route('/chat/messages')
def get_messages():
    user_id = int(request.cookies.get('userId'))
    target_id = int(request.args.get('target_id'))

    messages = MessageInfo.query.filter(
        ((MessageInfo.userId == user_id) & (MessageInfo.landlordId == target_id)) |
        ((MessageInfo.userId == target_id) & (MessageInfo.landlordId == user_id))
    ).order_by(MessageInfo.id.asc()).all()

    return jsonify([
        {
            'sender': msg.userId,
            'message': msg.message
        } for msg in messages
    ])


@chat_bp.route('/chat/send', methods=['POST'])
def send_message():
    sender_id = int(request.cookies.get('userId'))
    receiver_id = int(request.form.get('receiver_id'))
    message = request.form.get('message')

    new_msg = MessageInfo(
        userId=sender_id,
        landlordId=receiver_id,
        message=message,
        user_flag=0,
        landlord_flag=1
    )
    db.session.add(new_msg)
    db.session.commit()
    return jsonify({'status': 'ok'})

@chat_bp.route('/chat')
def chat_page():
    return render_template('landlord/chat_partial.html')  # 注意这里不是整个页面

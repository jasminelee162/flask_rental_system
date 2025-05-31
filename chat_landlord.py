# from flask import Blueprint, request, jsonify
# from models import db, MessageInfo, User
# from flask_login import current_user
#
# chat_landlord_bp = Blueprint('chat_landlord', __name__, url_prefix='/chat_landlord')
#
# @chat_landlord_bp.route('/list')
# def chat_list():
#     landlord_id = int(request.cookies.get('landlordId'))
#     # 查询所有跟该商 家有聊天记录的用户ID
#     records = MessageInfo.query.filter(MessageInfo.landlordId == landlord_id).all()
#
#     user_ids = set()
#     for record in records:
#         user_ids.add(record.userId)
#
#     users = User.query.filter(User.id.in_(user_ids)).all()
#     result = [{'id': u.id, 'name': u.name} for u in users]
#     return jsonify(result)
#
# @chat_landlord_bp.route('/messages')
# def get_messages():
#     landlord_id = int(request.cookies.get('landlordId'))
#     user_id = request.args.get('user_id', type=int)
#     if not user_id:
#         return jsonify({"error": "缺少user_id"}), 400
#
#     msgs = MessageInfo.query.filter(
#         ((MessageInfo.landlordId == landlord_id) & (MessageInfo.userId == user_id)) |
#         ((MessageInfo.landlordId == landlord_id) & (MessageInfo.userId == user_id))
#     ).order_by(MessageInfo.id.asc()).all()
#
#     result = []
#     for msg in msgs:
#         sender = msg.landlordId if msg.from_landlord else msg.userId
#         result.append({
#             "sender": sender,
#             "message": msg.message
#         })
#     return jsonify(result)
#
# @chat_landlord_bp.route('/send', methods=['POST'])
# def send_message():
#     landlord_id = int(request.cookies.get('landlordId'))
#     user_id = request.form.get('user_id', type=int)
#     message = request.form.get('message')
#
#     if not user_id or not message:
#         return jsonify({"error": "缺少参数"}), 400
#
#     # 商家发消息，from_landlord=1
#     new_msg = MessageInfo(
#         landlordId=landlord_id,
#         userId=user_id,
#         message=message,
#         user_flag=0,
#         landlord_flag=1
#     )
#     db.session.add(new_msg)
#     db.session.commit()
#
#     return jsonify({"status": "ok"})

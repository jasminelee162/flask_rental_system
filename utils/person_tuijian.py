from math import sqrt
from models import Tuijian
from sqlalchemy import func
from settings import db


def pearson_sim(user1_data, user2_data):
    """计算皮尔逊相关系数"""
    sum_xy = 0  # x*y之和
    sum_x = 0  # x之和
    sum_y = 0  # y之和
    sum_x2 = 0  # x平方之和
    sum_y2 = 0  # y平方之和
    n = 0  # 共同打分的个数

    for key in user1_data.keys():
        if key in user2_data.keys():  # 共同打分的物品
            n += 1
            x = user1_data[key]
            y = user2_data[key]
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_x2 += pow(x, 2)
            sum_y2 += pow(y, 2)

    if n == 0:
        return 0

    # 皮尔逊相关系数计算公式
    denominator = sqrt(sum_x2 - pow(sum_x, 2) / n) * sqrt(sum_y2 - pow(sum_y, 2) / n)
    if denominator == 0:
        return 0
    return (sum_xy - (sum_x * sum_y) / n) / denominator


def recommed(user_id):
    """基于用户的协同过滤推荐算法"""
    # 获取所有用户的浏览数据
    all_user_data = {}
    users = db.session.query(Tuijian.user_id).distinct().all()

    for user in users:
        user_scores = Tuijian.query.filter_by(user_id=user[0]).all()
        if user_scores:
            all_user_data[user[0]] = {score.house_id: score.score for score in user_scores}

    # 如果目标用户没有浏览记录，返回None
    if user_id not in all_user_data:
        return None

    # 计算目标用户与其他用户的相似度
    user_sim_scores = []
    for other_user_id, other_user_data in all_user_data.items():
        if other_user_id != user_id:
            similarity = pearson_sim(all_user_data[user_id], other_user_data)
            user_sim_scores.append((other_user_id, similarity))

    # 按相似度排序
    user_sim_scores.sort(key=lambda x: x[1], reverse=True)

    # 获取推荐房源
    recommendations = {}
    for other_user_id, similarity in user_sim_scores[:3]:  # 取前3个最相似的用户
        if similarity <= 0:
            continue

        for house_id, score in all_user_data[other_user_id].items():
            if house_id not in all_user_data[user_id]:  # 用户未浏览过的房源
                if house_id not in recommendations:
                    recommendations[house_id] = 0
                recommendations[house_id] += similarity * score

    # 将推荐结果按得分排序
    recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
    return recommendations[:6]  # 返回前6个推荐结果
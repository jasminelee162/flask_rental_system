# utils/pearson_tuijian.py

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
    n = 0  # 共同评分的数量

    for key in user1_data.keys():
        if key in user2_data.keys():  # 共同评分的项目
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

    # 计算皮尔逊相关系数
    denominator = sqrt(sum_x2 - pow(sum_x, 2) / n) * sqrt(sum_y2 - pow(sum_y, 2) / n)
    if denominator == 0:
        return 0
    return (sum_xy - (sum_x * sum_y) / n) / denominator


def recommed(user_id):
    """基于用户的协同过滤推荐算法"""
    # 获取所有用户的浏览记录
    user_views = {}
    all_views = Tuijian.query.all()

    # 构建用户-房源评分矩阵
    for view in all_views:
        if view.user_id not in user_views:
            user_views[view.user_id] = {}
        user_views[view.user_id][view.house_id] = view.score

    # 如果是新用户，返回热门房源
    if user_id not in user_views:
        hot_houses = db.session.query(
            Tuijian.house_id,
            func.count(Tuijian.id).label('view_count')
        ).group_by(Tuijian.house_id).order_by(
            func.count(Tuijian.id).desc()
        ).limit(5).all()
        return [h[0] for h in hot_houses]

    # 计算目标用户与其他用户的相似度
    user_sims = {}
    for other_id in user_views:
        if other_id != user_id:
            sim = pearson_sim(user_views[user_id], user_views[other_id])
            user_sims[other_id] = sim

    # 按相似度排序
    sorted_sims = sorted(user_sims.items(), key=lambda x: x[1], reverse=True)

    # 获取推荐房源
    rec_houses = set()
    for other_id, sim in sorted_sims[:3]:  # 取相似度最高的3个用户
        for house_id in user_views[other_id]:
            if house_id not in user_views[user_id]:  # 用户未看过的房源
                rec_houses.add(house_id)
                if len(rec_houses) >= 5:  # 最多推荐5个
                    break

    return list(rec_houses)
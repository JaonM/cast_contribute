# -*- coding:utf-8 -*-
"""
计算贡献度 及电影推荐
"""
import pymongo
import numpy as np
from model.box_office_predict import ridge_regression
import random
import pandas as pd
import xgboost as xgb

cast_portrait = pymongo.MongoClient('192.168.200.47', 27017)['Land_Movie']['cast_personas']


def predict_schedule_rate(director, actor1, actor2, actor3, actor4):
    """
    预测电影排片率
    :param director: 导演
    :param actor1:  演员1
    :param actor2:  演员2
    :param actor3:  演员3
    :param actor4: 演员4
    :return:
    """
    # director_influence = director['influence']
    # director_award_count = director['award_count']
    # director_weibo_pos = director['weibo_pos']
    # director_num_follow = director['num_follow']
    # director_num_tweets = director['num_tweets']
    # director_num_fan = director['num_fan']
    #
    # actor1_influence = actor1['influence']
    # actor1_award_count = actor1['award_count']
    # actor1_weibo_pos = actor1['weibo_pos']
    # actor1_num_follow = actor1['num_follow']
    # actor1_num_tweets = actor1['num_tweets']
    # actor1_num_fan = actor1['num_fan']
    #
    # actor2_influence = actor2['influence']
    # actor2_award_count = actor2['award_count']
    # actor2_weibo_pos = actor2['weibo_pos']
    # actor2_num_follow = actor2['num_follow']
    # actor2_num_tweets = actor2['num_tweets']
    # actor2_num_fan = actor2['num_fan']
    #
    # actor3_influence = actor3['influence']
    # actor3_award_count = actor3['award_count']
    # actor3_weibo_pos = actor3['weibo_pos']
    # actor3_num_follow = actor3['num_follow']
    # actor3_num_tweets = actor3['num_tweets']
    # actor3_num_fan = actor3['num_fan']
    #
    # actor4_influence = actor4['influence']
    # actor4_award_count = actor4['award_count']
    # actor4_weibo_pos = actor4['weibo_pos']
    # actor4_num_follow = actor4['num_follow']
    # actor4_num_tweets = actor4['num_tweets']
    # actor4_num_fan = actor4['num_fan']
    #
    # X = [director_influence, director_award_count, director_weibo_pos, director_num_follow, director_num_tweets,
    #      director_num_fan, actor1_influence, actor1_award_count, actor1_weibo_pos, actor1_num_follow, actor1_num_tweets,
    #      actor1_num_fan, actor2_influence, actor2_award_count, actor2_weibo_pos, actor2_num_follow, actor2_num_tweets,
    #      actor2_num_fan,
    #      actor3_influence, actor3_award_count, actor3_weibo_pos, actor3_num_follow, actor3_num_tweets, actor3_num_fan,
    #      actor4_influence,
    #      actor4_award_count, actor4_weibo_pos, actor4_num_follow, actor4_num_tweets, actor4_num_fan]
    #
    # rf_schedule = rf_schedule_rate.random_forest_schedule()
    # return rf_schedule.predict(X)

    # filter_features = [
    #     'director_influence', 'actor4_influence', 'director_overall', 'actor1_line_ability', 'actor1_figure',
    #     'actor3_acting', 'actor2_influence', 'actor2_voice', 'actor1_voice', 'actor3_influence', 'actor4_appearance',
    #     'actor1_influence', 'actor4_line_ability', 'actor3_voice', 'actor4_figure', 'actor2_acting', 'actor3_figure',
    #     'actor2_line_ability', 'actor2_figure', 'actor4_acting', 'actor1_acting', 'actor2_appearance',
    #     'actor3_line_ability', 'actor1_appearance', 'actor4_voice', 'actor3_appearance', 'actor1_award_count',
    #     'actor3_award_count', 'actor4_award_count'
    # ]
    director_influence = director['influence']
    actor4_influence = actor4['influence']
    director_overall = director['director_overall']
    actor1_line_ability = actor1['line_ability']
    actor1_figure = actor1['figure']
    actor3_acting = actor3['acting']
    actor2_influence = actor2['influence']
    actor2_voice = actor2['voice']
    actor1_voice = actor1['voice']
    actor3_influence = actor3['influence']
    actor4_appearance = actor4['appearance']
    actor1_influence = actor1['influence']
    actor4_line_ability = actor4['line_ability']
    actor3_voice = actor3['voice']
    actor4_figure = actor4['figure']
    actor2_acting = actor2['acting']
    actor3_figure = actor3['figure']
    actor2_line_ability = actor2['line_ability']
    actor2_figure = actor2['figure']
    actor4_acting = actor4['acting']
    actor1_acting = actor1['acting']
    actor2_appearance = actor2['appearance']
    actor3_line_ability = actor3['line_ability']
    actor1_appearance = actor1['appearance']
    actor4_voice = actor4['voice']
    actor3_appearance = actor3['appearance']
    actor1_award_count = actor1['award_count']
    actor3_award_count = actor3['award_count']
    actor4_award_count = actor4['award_count']

    X = [director_influence, actor4_influence, director_overall, actor1_line_ability, actor1_figure, actor3_acting,
         actor2_influence, actor2_voice, actor1_voice, actor3_influence, actor4_appearance, actor1_influence,
         actor4_line_ability, actor3_voice, actor4_figure, actor2_acting, actor3_figure, actor2_line_ability,
         actor2_figure, actor4_acting, actor1_acting, actor2_appearance, actor3_line_ability, actor1_appearance,
         actor4_voice,
         actor3_appearance, actor1_award_count, actor3_award_count, actor4_award_count]

    bst = xgb.Booster()
    bst.load_model('../contribute_model/schedule_rate_predict.model')
    y = bst.predict(xgb.DMatrix(X))

    return y


def predict_want_count(director, actor1, actor2, actor3, actor4):
    # director_influence = director['influence']
    # director_award_count = director['award_count']
    # director_weibo_pos = director['weibo_pos']
    # director_num_follow = director['num_follow']
    # director_num_tweets = director['num_tweets']
    # director_num_fan = director['num_fan']
    #
    # actor1_influence = actor1['influence']
    # actor1_award_count = actor1['award_count']
    # actor1_weibo_pos = actor1['weibo_pos']
    # actor1_num_follow = actor1['num_follow']
    # actor1_num_tweets = actor1['num_tweets']
    # actor1_num_fan = actor1['num_fan']
    #
    # actor2_influence = actor2['influence']
    # actor2_award_count = actor2['award_count']
    # actor2_weibo_pos = actor2['weibo_pos']
    # actor2_num_follow = actor2['num_follow']
    # actor2_num_tweets = actor2['num_tweets']
    # actor2_num_fan = actor2['num_fan']
    #
    # actor3_influence = actor3['influence']
    # actor3_award_count = actor3['award_count']
    # actor3_weibo_pos = actor3['weibo_pos']
    # actor3_num_follow = actor3['num_follow']
    # actor3_num_tweets = actor3['num_tweets']
    # actor3_num_fan = actor3['num_fan']
    #
    # actor4_influence = actor4['influence']
    # actor4_award_count = actor4['award_count']
    # actor4_weibo_pos = actor4['weibo_pos']
    # actor4_num_follow = actor4['num_follow']
    # actor4_num_tweets = actor4['num_tweets']
    # actor4_num_fan = actor4['num_fan']
    #
    # X = [director_influence, director_award_count, director_weibo_pos, director_num_follow, director_num_tweets,
    #      director_num_fan, actor1_influence, actor1_award_count, actor1_weibo_pos, actor1_num_follow, actor1_num_tweets,
    #      actor1_num_fan, actor2_influence, actor2_award_count, actor2_weibo_pos, actor2_num_follow, actor2_num_tweets,
    #      actor2_num_fan,
    #      actor3_influence, actor3_award_count, actor3_weibo_pos, actor3_num_follow, actor3_num_tweets, actor3_num_fan,
    #      actor4_influence,
    #      actor4_award_count, actor4_weibo_pos, actor4_num_follow, actor4_num_tweets, actor4_num_fan]
    #
    # rf = rf_want_count.random_forest_want_count()
    # return rf.predict(X)
    df_movie = pd.read_csv('../../input/movie_feature.csv', encoding='utf-8')
    want_count = df_movie['want_count']
    want_count.fillna('0', inplace=True)
    return want_count.mean()


def predict_score(director, actor1, actor2, actor3, actor4):
    # director_influence = director['influence']
    # director_award_count = director['award_count']
    # director_weibo_pos = director['weibo_pos']
    # director_num_follow = director['num_follow']
    # director_num_tweets = director['num_tweets']
    # director_num_fan = director['num_fan']
    #
    # actor1_influence = actor1['influence']
    # actor1_award_count = actor1['award_count']
    # actor1_weibo_pos = actor1['weibo_pos']
    # actor1_num_follow = actor1['num_follow']
    # actor1_num_tweets = actor1['num_tweets']
    # actor1_num_fan = actor1['num_fan']
    #
    # actor2_influence = actor2['influence']
    # actor2_award_count = actor2['award_count']
    # actor2_weibo_pos = actor2['weibo_pos']
    # actor2_num_follow = actor2['num_follow']
    # actor2_num_tweets = actor2['num_tweets']
    # actor2_num_fan = actor2['num_fan']
    #
    # actor3_influence = actor3['influence']
    # actor3_award_count = actor3['award_count']
    # actor3_weibo_pos = actor3['weibo_pos']
    # actor3_num_follow = actor3['num_follow']
    # actor3_num_tweets = actor3['num_tweets']
    # actor3_num_fan = actor3['num_fan']
    #
    # actor4_influence = actor4['influence']
    # actor4_award_count = actor4['award_count']
    # actor4_weibo_pos = actor4['weibo_pos']
    # actor4_num_follow = actor4['num_follow']
    # actor4_num_tweets = actor4['num_tweets']
    # actor4_num_fan = actor4['num_fan']
    #
    # X = [director_influence, director_award_count, director_weibo_pos, director_num_follow, director_num_tweets,
    #      director_num_fan, actor1_influence, actor1_award_count, actor1_weibo_pos, actor1_num_follow, actor1_num_tweets,
    #      actor1_num_fan, actor2_influence, actor2_award_count, actor2_weibo_pos, actor2_num_follow, actor2_num_tweets,
    #      actor2_num_fan,
    #      actor3_influence, actor3_award_count, actor3_weibo_pos, actor3_num_follow, actor3_num_tweets, actor3_num_fan,
    #      actor4_influence,
    #      actor4_award_count, actor4_weibo_pos, actor4_num_follow, actor4_num_tweets, actor4_num_fan]
    #
    # rf = rf_score.random_forest_score()
    # return rf.predict(X)

    director_influence = director['influence']
    actor1_figure = actor1['figure']
    director_overall = director['director_overall']
    actor4_influence = actor4['influence']
    actor2_voice = actor2['voice']
    actor2_line_ability = actor2['line_ability']
    actor2_acting = actor2['acting']
    actor1_influence = actor1['influence']
    actor1_acting = actor1['acting']
    actor4_acting = actor4['acting']
    actor3_figure = actor3['figure']
    actor3_appearance = actor3['appearance']
    actor1_voice = actor1['voice']
    actor3_voice = actor3['voice']
    actor4_appearance = actor4['appearance']
    actor1_line_ability = actor1['line_ability']
    actor2_figure = actor2['figure']
    actor4_figure = actor4['figure']
    actor2_appearance = actor2['appearance']
    actor4_line_ability = actor4['line_ability']
    actor3_acting = actor3['acting']
    actor4_voice = actor4['voice']
    actor1_appearance = actor1['appearance']
    actor3_line_ability = actor3['line_ability']
    actor3_influence = actor3['influence']

    X = [director_influence, actor1_figure, director_overall, actor4_influence, actor2_voice, actor2_line_ability,
         actor2_acting, actor1_influence, actor1_acting, actor4_acting, actor3_figure, actor3_appearance, actor1_voice,
         actor3_voice, actor4_appearance, actor1_line_ability, actor2_figure, actor4_figure, actor2_appearance,
         actor4_line_ability, actor3_acting, actor4_voice, actor1_appearance, actor3_line_ability, actor3_influence]

    bst = xgb.Booster()
    bst.load_model('../contribute_model/score_predict.model')
    y = bst.predict(xgb.DMatrix(X))
    return y


def compute_contribute(movie_budget, movie_type, is_hot_schedule, is_serie, production_company, director, actor1,
                       actor2, actor3,
                       actor4):
    """
    计算贡献度 (投资回报比)
    :param movie_budget:
    :param movie_type: type array
    :param is_hot_schedule: 0 1
    :param production_company: company array
    :param director:
    :param actor1:
    :param actor2:
    :param actor3:
    :param actor4:
    :return:
    """
    companys = ['中国电影股份有限公司', '华夏电影发行有限责任公司', '中国电影集团公司', '万达影视传媒有限公司', '华谊兄弟传媒股份有限公司']
    types = ['剧情', '动作', '爱情', '喜剧', '奇幻', '冒险', '犯罪', '悬疑', '惊悚']

    try:
        director = cast_portrait.find({'name': director})[0]
        actor1 = cast_portrait.find({'name': actor1})[0]
        actor2 = cast_portrait.find({'name': actor2})[0]
        actor3 = cast_portrait.find({'name': actor3})[0]
        actor4 = cast_portrait.find({'name': actor4})[0]
    except:
        return '暂未收入所需主创的画像数据，模型退出'
        # try:
    X = [is_hot_schedule]
    schedule_rate = predict_schedule_rate(director, actor1, actor2, actor3, actor4)
    # X = np.concatenate([X, [schedule_rate], [is_serie]])
    X.extend([schedule_rate[0], is_serie])
    # print(schedule_rate[0])
    want_count = predict_want_count(director, actor1, actor2, actor3, actor4)
    score = predict_score(director, actor1, actor2, actor3, actor4)
    print(score)
    # print(X)
    # X = np.concatenate([X, want_count])
    # X = np.concatenate([X, score])
    X.extend([want_count, score[0]])
    for i in range(len(types)):
        if types[i] in movie_type:
            X = np.hstack([X, [1]])
        else:
            X = np.hstack([X, [0]])

    is_company = False
    for i in range(len(companys)):
        if companys[i] in production_company:
            X = np.hstack([X, [1]])
            is_company = True
        else:
            X = np.hstack([X, [0]])
    if is_company:
        X = np.hstack([X, [0]])
    else:
        X = np.hstack([X, [1]])

    ridge = ridge_regression.box_office_ridge()
    box_office = ridge.predict(X)
    print('票房: ' + str(box_office[0]))
    contribute = (box_office[0] * 0.43 - movie_budget) / movie_budget
    print('贡献度ROI: ' + str(contribute))

    # except:
    #     print('计算贡献度出错,画像数据缺失')
    #     return 0

    movie_box = pymongo.MongoClient('192.168.200.47', 27017)['Land_Movie']['movie_box']
    movie_type = str(movie_type).replace('[', '')
    movie_type=movie_type.replace(']', '')
    production_company = str(production_company).replace('[', '')
    production_company=production_company.replace(']', '')
    if is_hot_schedule == 1:
        is_hot_schedule = 'YES'
    else:
        is_hot_schedule = 'NO'
    if is_serie == 1:
        is_serie = 'YES'
    else:
        is_serie = 'NO'
    movie_box.insert_one({'Publisher': production_company, 'movie_type': movie_type, 'isSequel': is_serie,
                          'is_GoldType': is_hot_schedule, 'Director': director['name'], 'actor1': actor1['name'],
                          'actor2': actor2['name'], 'actor3': actor3['name'], 'actor4': actor4['name'],
                          'movie_budget': movie_budget, 'box_office': box_office[0]})
    return box_office, contribute


"""

输出贡献度为
票房: 529404248.215
贡献度ROI: 1.27643826733
"""

compute_contribute(movie_budget=10000000, movie_type=['科幻', '冒险'], is_hot_schedule=0, is_serie=0,
                   production_company=['中国电影股份有限公司'], director='周星驰', actor1='范冰冰', actor2='赵丽颖', actor3='陈赫',
                   actor4='赵薇')


def recommend_cast(movie_budget, movie_type, is_hot_schedule, is_serie, production_company, iter=1000):
    """

    :param movie_budget:
    :param movie_type:
    :param is_hot_schedule:
    :param is_serie:
    :param production_company:
    :param iter:
    :return:
    """
    directors = cast_portrait.find({'occupation': {'$regex': '导演'}})
    actors = cast_portrait.find({'occupation': {'$regex': '演员'}})
    director_count = directors.count()
    actor_count = actors.count()
    max_contribute = 0
    cast_dict = dict()
    for round in range(iter):
        try:
            _one = directors[random.randint(0, director_count)]
            _two = actors[random.randint(0, actor_count)]
            _three = actors[random.randint(0, actor_count)]
            _four = actors[random.randint(0, actor_count)]
            _five = actors[random.randint(0, actor_count)]
        except:
            continue

        try:
            box_office, contribute = compute_contribute(movie_budget, movie_type, is_hot_schedule, is_serie,
                                                        production_company,
                                                        _one['name'], _two['name'], _three['name'], _four['name'],
                                                        _five['name'])
        except KeyError:
            continue
        if box_office > max_contribute:
            max_contribute = contribute
            cast_dict['director'] = _one['name']
            cast_dict['actor1'] = _two['name']
            cast_dict['actor2'] = _three['name']
            cast_dict['actor3'] = _four['name']
            cast_dict['actor4'] = _five['name']

    recommend = pymongo.MongoClient('192.168.200.47', 27017)['Land_Movie']['recommend']
    movie_type = str(movie_type).replace('[', '')
    movie_type = movie_type.replace(']', '')
    production_company = str(production_company).replace('[', '')
    production_company = production_company.replace(']', '')
    if is_hot_schedule == 1:
        is_hot_schedule = 'YES'
    else:
        is_hot_schedule = 'NO'
    if is_serie == 1:
        is_serie = 'YES'
    else:
        is_serie = 'NO'

    recommend.insert_one({'Publisher': production_company, 'movie_type': movie_type, 'isSequel': is_serie,
                          'is_GoldType': is_hot_schedule, 'Director': _one['name'], 'actor1': _two['name'],
                          'actor2': _three['name'], 'actor3': _four['name'], 'actor4': _five['name'],
                          'movie_budget': movie_budget, })
    print("最大贡献度: " + str(max_contribute))
    print("推荐主创名单: " + str(cast_dict))


"""
输出
最大贡献度: 35.1318184382
推荐主创名单: {'actor2': '姜仁衍', 'actor4': '孙宁', 'director': '弗兰', 'actor1': 'Gilles Cohen', 'actor3': '张博宇'}
"""
# recommend_cast(movie_budget=10000000, movie_type='冒险', is_hot_schedule=1, is_serie=1,
#                production_company=['中国电影股份有限公司'], iter=1000)

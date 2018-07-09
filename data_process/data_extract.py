# -*- coding: utf-8 -*-
"""
从原始数据库中获取数据
"""
import pymongo
import pandas as pd
import datetime

movie_id = 10000

client = pymongo.MongoClient('192.168.200.47', 27017)

YPE = client['Land_Movie']['YPEMovie']

result = []

hot_schedule = [
    {'start': {'month': 1, 'day': 1}, 'end': {'month': 2, 'day': 30}},
    {'start': {'month': 5, 'day': 1}, 'end': {'month': 5, 'day': 7}},
    {'start': {'month': 6, 'day': 1}, 'end': {'month': 8, 'day': 31}},
    {'start': {'month': 10, 'day': 1}, 'end': {'month': 10, 'day': 7}},
    {'start': {'month': 11, 'day': 20}, 'end': {'month': 12, 'day': 31}},
]

columns = ['movie_id', 'box_office', 'movie_name', 'production_company', 'is_hot_schedule', 'director', 'actors',
           'schedule_rate',
           'box_office_rate', 'movie_type', 'is_series', 'ypr_want_count', 'ypr_score', 'douban_want_count',
           'douban_score', 'maoyan_want_count', 'maoyan_score', 'taopiaopiao_want_count', 'taopiaopiao_score',
           'nuomi_want_count', 'nuomi_score', 'shiguang_want_count', 'shiguang_score', 'languages',
           'director_award_count', 'actor_award_count']

# columns = ['movie_id', 'box_office', 'movie_name', 'is_hot_schedule', 'director', 'actors', 'director_award_count',
#            'actor_award_count']

# columns = ['movie_id', 'box_office', 'movie_name', 'is_hot_schedule', 'director', 'actors']

# for doc in YPE.find():
_cursor = YPE.find(no_cursor_timeout=True)
for doc in _cursor:
    movie_id += 1
    movie = dict()
    movie['movie_id'] = movie_id
    movie['box_office'] = doc['total_boxoffice']
    movie['movie_name'] = doc['movie_name']
    production_company = ''
    try:
        for company in doc['production_company']:
            production_company += company
            production_company += ','
        production_company = production_company[:-1]
    except KeyError:
        pass
    movie['production_company'] = production_company
    # movie = {'movie_id': ++movie_id, 'movie_name': doc['movie_name']}
    try:
        release_date = datetime.datetime.strptime(doc['release_date'], '%Y-%m-%d')
        is_hot_schedule = 0
        # print(release_date)
        for schedule in hot_schedule:
            if schedule['start']['month'] <= release_date.month <= schedule['end']['month'] and \
                                    schedule['start']['day'] <= release_date.day <= schedule['end']['day']:
                # print(release_date.month)
                is_hot_schedule = 1
                break
            else:
                is_hot_schedule = 0
    except KeyError:
        is_hot_schedule = 0
    movie['is_hot_schedule'] = is_hot_schedule
    # 获取导演
    movie['director'] = doc['director']
    #
    # # 获取演员
    movie['actors'] = doc['actor'].replace('/', ',')
    #
    # 获取平均票价,平均排片率
    schedule_rate = 0
    box_office_rate = 0
    count_1 = 0
    count_2 = 0
    for trend in doc['movie_trend']:
        try:
            schedule_rate += trend['schedule_rate']
            count_1 += 1
        except KeyError:
            schedule_rate += 0
        try:
            box_office_rate += trend['box_office_rate']
            count_2 += 1
        except:
            box_office_rate += 0
    if count_1 != 0:
        movie['schedule_rate'] = schedule_rate / count_1
    if count_2 != 0:
        movie['box_office_rate'] = box_office_rate / count_2

    movie['movie_type'] = doc['movie_type'].replace('/', ',')

    # 是否有前作
    movie['is_series'] = 0

    for want in doc['movie_want']:
        platform = want['platform']
        if platform == '娱票儿':
            try:
                want_count = want['want']
            except KeyError:
                want_count = 0

        else:
            try:
                want_count = want['want_number']
            except KeyError:
                want_count = 0
        if platform == '娱票儿':
            platform = 'ypr'
        elif platform == '豆瓣':
            platform = 'douban'
        elif platform == '猫眼':
            platform = 'maoyan'
        elif platform == '淘票票':
            platform = 'taopiaopiao'
        elif platform == '糯米':
            platform = 'nuomi'
        elif platform == '时光网':
            platform = 'shiguang'
        movie[platform + '_want_count'] = want_count
        try:
            score = want['score']
        except KeyError:
            score = 0
        movie[platform + '_score'] = score

        try:
            movie['ypr_score'] = doc['score']
        except:
            pass

            #  查询电影语种
    for doc in client['Land_Movie']['douban_sub'].find():
        try:
            if doc['name'] == movie['movie_name']:

                break
            else:
                continue
        except KeyError:
            continue

    cursor = client['Land_Movie']['douban_sub'].find({'name': movie['movie_name']})
    if cursor.count() > 0:
        doc = cursor[0]
        la = ''
        try:
            for lang in doc['languages']:
                la += lang
                la += ','
            la = la[:-1]
        except:
            pass
        movie['languages'] = la
        movie['douban_want_count'] = doc['wish']

    director_award_count = 0
    # 查询导演获奖平均数量
    for director in movie['director'].split('/'):
        print(director)
        cursor = client['Land_Movie']['baike'].find({'chinese_name': director.strip()})
        if cursor.count() > 0:
            print('here')
            try:
                director_award_count += len(cursor[0]['awards'])
                print(director_award_count)
            except KeyError:
                director_award_count = 0
    director_award_count = director_award_count / len(movie['director'].split('/'))
    movie['director_award_count'] = director_award_count

    actor_award_count = 0
    # 查询演员获奖平均数量
    for actor in movie['actors'].split(','):
        cursor = client['Land_Movie']['baike'].find({'chinese_name': actor.strip()})
        if cursor.count() > 0:
            try:
                actor_award_count += len(cursor[0]['awards'])
            except KeyError:
                actor_award_count = 0
    actor_award_count = director_award_count / len(movie['actors'].split(','))
    movie['actor_award_count'] = actor_award_count

    result.append(movie)
_cursor.close()

df = pd.DataFrame(data=result, columns=columns)

df.to_csv('movie.csv', index=False, encoding='utf-8')

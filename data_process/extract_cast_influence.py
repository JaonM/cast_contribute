# -*- coding:utf-8 -*-
"""
用主创近年平均票房拟合主创影响力
"""
import pymongo
import pandas as pd
import codecs

cast_portrait = pymongo.MongoClient('192.168.200.47', 27017)['Land_Movie']['cast_portrait']
cast_list = []

file = codecs.open('../model/word_bank/key.txt', encoding='utf-8')
for line in file.readlines():
    cast_list.append(line.strip())

client = pymongo.MongoClient('192.168.200.47', 27017)
YPE = client['Land_Movie']['YPEMovie']

result = []
id = 0
for cast in cast_list:
    print(id)
    id += 1
    count = 0
    box_office = 0
    for doc in YPE.find():
        is_in = False
        try:
            if cast in doc['actor']:
                is_in = True
        except KeyError:
            pass
        try:
            if cast in doc['director']:
                is_in = True
        except KeyError:
            pass
        if is_in and doc['total_boxoffice'] != '-':
            box_office += doc['total_boxoffice']
            count += 0
    if count != 0:
        box_office = box_office / count
    result.append({'name': cast, 'influence': box_office})

df = pd.DataFrame(result, columns=['name', 'influence'])
df.to_csv('../input/cast_avg_box_office.csv', index=False, encoding='utf-8')

movie_raw = pd.read_csv('../input/movie_raw.csv')
# cast_influence = pd.read_csv('../input/cast_avg_box_office.csv')

result = []
for index, item in movie_raw.iterrows():
    print(index)
    try:
        directors = item['director'].split('/')
    except:
        directors = []
    dir_influence = 0
    for dir in directors:
        cursor = cast_portrait.find({'name': dir})
        if cursor.count() > 0:
            dir_influence += cursor[0]['influence']
            # for index, i in cast_influence.iterrows():
            #     name = i['name']
            #     if dir == name:
            #         dir_influence += i['influence']
            #         break
    dir_influence = dir_influence / (len(directors) + 0.01)
    try:
        actors = item['actors'].split(',')
    except:
        actors = []
    # 前4为演员平均票房
    act_influence = 0
    act_count = 0
    for act in actors:
        act_count += 1
        if act_count > 4:
            break
        # for index, i in cast_influence.iterrows():
        #     name = i['name']
        #     if act == name:
        #         act_influence += i['influence']
        #         break
        cursor = cast_portrait.find({'name': act})
        if cursor.count() > 0:
            act_influence += cursor[0]['influence']
    act_influence = act_influence / (act_count + 0.01)

    result.append({'movie_id': item['movie_id'], 'director_influence': dir_influence, 'actor_influence': act_influence})

df = pd.DataFrame(result, columns=['movie_id', 'director_influence', 'actor_influence'])
df.to_csv('../input/cast_influence.csv', index=False, encoding='utf-8')

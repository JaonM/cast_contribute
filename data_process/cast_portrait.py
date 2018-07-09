# -*- coding:utf-8 -*-
"""
创建主创画像
"""
import pymongo
import pandas as pd
import random
import re

client = pymongo.MongoClient('192.168.200.47', 27017)
db = client['Land_Movie']
col = db['cast_personas']

# senti_portrait = pd.read_csv('../input/cast_sentiment_portrait.csv')
# cast_avg_box = pd.read_csv('../input/cast_avg_box_office.csv')
# fubusi = pd.read_csv('../input/fubusi_portrait.csv')
#
# portrait = pd.merge(senti_portrait, cast_avg_box, left_on='cast_name', right_on='name')
#
# portrait = pd.merge(portrait, fubusi, left_on='cast_name', right_on='name', how='outer')

portrait = pd.read_csv('../input/cast_portrait.csv', encoding='utf-8')
portrait['occupation'].fillna('演员')
print(portrait)
# portrait.to_csv('../input/cast_portrait.csv', index=False, encoding='utf-8')

# for index, item in portrait.iterrows():
#     if col.find({'name': item['cast_name']}).count() > 0:
#         continue
#     col.insert_one({'name': item['cast_name'], 'occupation': item['occupation'], 'weibo_pos': item['weibo_pos'],
#                     'award_count': item['award_count'],
#                     'num_fan': item['num_fan'], 'num_follow': item['num_follow'], 'num_tweets': item['num_tweets'],
#                     'influence': item['influence'], 'income': item['income']})

"""
增加主创画像数据、存入数据库
"""
for doc in col.find():
    _id = doc['_id']
    occupation = str(doc['occupation'])
    # print(type(occupation))
    if re.search('导演', occupation):
        movie_pace = random.uniform(2.5, 4.5)
        character = random.uniform(2.5, 4.5)
        director_overall = random.uniform(2.5, 4.5)
        d = doc
        d['movie_pace'] = movie_pace
        d['character'] = character
        d['director_overall'] = director_overall
        # col.update({'id': _id},
        #            {'$set': {'movie_pace': movie_pace, 'character': character, 'director_overall': director_overall}})
        col.save(d)
    elif re.search('编剧', occupation):
        script = random.uniform(3, 4.5)
        scenarist_overall = random.uniform(3, 4.5)
        # col.update({'id': _id},
        #            {'$set': {'script': script, 'scenarist_overall': scenarist_overall}})
        d = doc
        d['script'] = script
        d['scearist_overall'] = scenarist_overall
        col.save(d)
    else:
        acting = random.uniform(3, 4.5)
        appearence = random.uniform(3, 4.5)
        figure = random.uniform(3, 4.5)
        voice = random.uniform(3, 4.5)
        temperament = random.uniform(3, 4.5)
        line_ability = random.uniform(3, 4.5)
        actor_overall = random.uniform(3, 4.5)

        d = doc
        d['acting'] = acting
        d['appearance'] = appearence
        d['figure'] = figure
        d['voice'] = voice
        d['temperament'] = temperament
        d['line_ability'] = line_ability
        d['actor_overall'] = actor_overall
        # col.update({'id': _id},
        #            {'$set': {'acting': acting, 'appearance': appearence, 'figure': figure, 'voice': voice,
        #                      'temperament': temperament, 'line_ability': line_ability, 'actor_overall': actor_overall}})
        col.save(d)

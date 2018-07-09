# -*- coding:utf-8 -*-
"""
抽取主创作为关键词
"""
import pymongo
import codecs
import pandas as pd

client = pymongo.MongoClient('192.168.200.47', 27017)
YPE = client['Land_Movie']['YPEMovie']

casts = []

df = pd.read_csv('../input/mainland_movie.csv', encoding='utf-8')

mainland_movie = []
# for doc in YPE.find():
#     count = 0
#     if doc['district'] == '中国大陆' or doc['district'] == '香港' or doc['district'] == '台湾':
#         mainland_movie.append(doc['movie_name'])
#         for actor in doc['actor'].split('/'):
#             casts.append(actor)
#             count += 1
#             if count > 3:
#                 break
#         for director in doc['director'].split('/'):
#             casts.append(director)

for index, item in df.iterrows():
    doc = YPE.find({'movie_name': item['movie_name']})[0]
    count = 0
    # if doc['district'] == '中国大陆' or doc['district'] == '香港' or doc['district'] == '台湾':
    mainland_movie.append(doc['movie_name'])
    for actor in doc['actor'].split('/'):
        casts.append(actor)
        count += 1
        if count > 3:
            break
    director = doc['director'].split('/')[0]
    casts.append(director)  # cast = list(set(casts))

new_cast = []

for cast in casts:
    if cast.strip() not in new_cast:
        new_cast.append(cast.strip())

with codecs.open('../model/word_bank/key.txt', 'w', encoding='utf-8') as file:
    for cast in new_cast:
        file.write(cast.strip() + '\n')

# df = pd.DataFrame(mainland_movie, columns=['movie_name'])
# df = df.to_csv('../input/mainland_movie.csv', encoding='utf-8', index=False)

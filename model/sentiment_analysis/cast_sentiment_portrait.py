# -*- coding:utf-8 -*-
"""
主创用户画像

基本信息、获奖数量、粉丝数量、微博正面率(负面率)...
"""

import pymongo
import pandas as pd
import codecs
from model.sentiment_analysis.senti_rule_based import weibo_analysis
import re
import json

client = pymongo.MongoClient('192.168.200.47', 27017)
db = client['Land_Movie']
cast_list = []

with codecs.open('../word_bank/key.txt', encoding='utf-8') as file:
    for line in file.readlines():
        l = line.strip()
        if l != '\n':
            cast_list.append(l)


# print(len(cast_list))
# print(cast_list)

# 分析微博情感分析
def weibo_sentiment():
    analysis = weibo_analysis()
    df_weibo = pd.read_csv('../../input/weibo_filtered.csv')
    # print(df_weibo['content'].duplicated())

    # 去重
    df_weibo['content'].drop_duplicates(inplace=True)

    cast_pos = dict()
    cast_neg = dict()
    for weibo in df_weibo['content'].values:
        weibo = re.sub('#.*#', '', weibo).replace('@', '')
        print(weibo)
        pos, neg = analysis.analyse_sentiment(weibo)
        if len(pos) != 0:
            for p in pos:
                cast_pos[p] = cast_pos.get(p, 0) + 1
        if len(neg) != 0:
            for n in neg:
                cast_neg[n] = cast_neg.get(n, 0) + 1
    return cast_pos, cast_neg


# cast_pos, cast_neg = weibo_sentiment()
#
# with open('../../input/cast_pos.txt', mode='w', encoding='utf-8') as file:
#     file.write(str(cast_pos))
# with open('../../input/cast_neg.txt', mode='w', encoding='utf-8') as file:
#     file.write(str(cast_neg))

with open('../../input/cast_pos.txt', encoding='utf-8') as file:
    cast_pos = json.loads(file.readline().strip().replace("'", '"'))

with open('../../input/cast_neg.txt', encoding='utf-8') as file:
    cast_neg = json.loads(file.readline().strip().replace("'", '"'))

cast_info = []

id = 0
for cast in cast_list:
    print(id)
    id += 1
    c = dict()
    c['cast_name'] = cast
    print(cast)
    cursor = db['baike'].find({'chinese_name': cast})
    occupation = ''
    award_count = 0
    if cursor.count() > 0:
        try:
            occupation = cursor[0]['occupation']
        except KeyError:
            pass
        try:
            award_count = len(cursor[0]['awards'])
        except KeyError:
            pass
    cursor.close()
    c['occupation'] = occupation

    # 获奖数量
    c['award_count'] = award_count

    # 微博正面率
    try:
        # c['weibo_pos'] = (cast_pos[cast] + 0.01) / (cast_neg[cast] + 0.01)
        pos = cast_pos[cast]
    except KeyError:
        pos = 1
    try:
        neg = cast_neg[cast]
    except KeyError:
        neg = 1
    c['weibo_pos'] = (pos + 0.01) / (pos + neg + 0.02)
    cursor = client['Sina']['Information'].find({'NickName': {'$regex': cast}})
    num_fan = 0
    num_follow = 0
    num_tweets = 0
    if cursor.count() > 0:
        max_doc = cursor[0]
        for doc in cursor:
            try:
                num_fan = doc['Num_Fans']
                if max_doc['Num_Fans'] < num_fan:
                    max_doc = doc
            except KeyError:
                continue
        try:
            num_fan = max_doc['Num_Fans']
        except KeyError:
            num_fan = 0
        try:
            num_follow = max_doc['Num_Follows']
        except KeyError:
            num_follow = 0
        try:
            num_tweets = max_doc['Num_Tweets']
        except KeyError:
            num_tweets = 0
    cursor.close()
    c['num_fan'] = num_fan
    c['num_follow'] = num_follow
    c['num_tweets'] = num_tweets

    cast_info.append(c)

df_cast = pd.DataFrame(cast_info,
                       columns=['cast_name', 'occupation', 'award_count', 'weibo_pos', 'num_fan', 'num_follow',
                                'num_tweets'])
df_cast.to_csv('../../input/cast_sentiment_portrait.csv', index=False, encoding='utf-8')

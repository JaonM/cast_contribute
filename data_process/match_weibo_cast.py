# -*- coding:utf-8 -*-
"""
匹配电影主创
"""
import pandas as pd
import pymongo

client = pymongo.MongoClient('192.168.200.47', 27017)

cast_weibo = pd.read_csv('../input/cast_new_match.csv', encoding='utf-8')

cast_weibo.fillna(0)

col = client['Land_Movie']['cast_personas']
#
# for index, item in cast_weibo.iterrows():
#     name = item['real_name']
#     print(name)
#     try:
#         doc = col.find({'name': name})[0]
#     except:
#         continue
#     average_attitudes_count = item['average_attitudes_count']
#     average_comments_count = item['average_comments_count']
#     average_followers_count = item['average_followers_count']
#     average_follow_count = item['average_follow_count']
#     average_reports_count = item['average_reports_count']
#
#     doc['average_attitudes_count'] = average_attitudes_count
#     doc['average_comments_count'] = average_comments_count
#     doc['average_followers_count'] = average_followers_count
#     doc['average_follow_count'] = average_follow_count
#     doc['average_reports_count'] = average_reports_count
#
#     col.save(doc)

for doc in col.find():
    try:
        average_attitudes_count=doc['average_attitudes_count']
    except KeyError:
        average_attitudes_count=0
    try:
        average_comments_count=doc['average_comments_count']
    except KeyError:
        average_comments_count=0
    try:
        average_followers_count = doc['average_followers_count']
    except KeyError:
        average_followers_count = 0
    try:
        average_follow_count=doc['average_follow_count']
    except KeyError:
        average_follow_count=0
    try:
        average_reports_count = doc['average_reports_count']
    except KeyError:
        average_reports_count=0
    doc['average_attitudes_count'] = average_attitudes_count
    doc['average_comments_count'] = average_comments_count
    doc['average_followers_count'] = average_followers_count
    doc['average_follow_count'] = average_follow_count
    doc['average_reports_count'] = average_reports_count

    col.save(doc)
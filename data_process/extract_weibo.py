# -*- coding:utf-8 -*-
"""
从数据库中导出微博数据
"""
import pymongo
import pandas as pd

client = pymongo.MongoClient('192.168.200.47', 27017)

weibo = client['Sina']['Tweets']

weibo_list = []

for doc in weibo.find():
    weibo_list.append({'weibo_id': doc['_id'], 'content': doc['Content'], 'time': doc['PubTime']})

df_weibo = pd.DataFrame(weibo_list, columns=['weibo_id', 'content', 'time'])
df_weibo.to_csv('../input/weibo.csv', index=False, encoding='utf-8')

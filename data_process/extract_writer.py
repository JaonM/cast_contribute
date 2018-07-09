"""
提取编剧特征
"""
import pymongo
import pandas as pd

client = pymongo.MongoClient('192.168.200.47', 27017)

YPE = client['Land_Movie']['YPEMovie']

douban = client['Land_Movie']['douban_1']

writers = []

for doc in YPE.find():
    movie_name = doc['movie_name']
    cursor = douban.find({'name': movie_name})
    if cursor.count() > 0:
        for writer in cursor[0]['screenwriter']:
            writers.append(writer)

writers=list(set(writers))
df = pd.DataFrame(writers, columns=['writer_name'])
df.to_csv('writer.csv', index=False, encoding='utf-8')

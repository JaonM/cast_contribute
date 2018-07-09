# -*- coding:utf-8 -*-
"""
过滤微博
"""
import pandas as pd
import codecs

weibo = pd.read_csv('../../input/weibo.csv')

cast_list = []
file = codecs.open('../word_bank/key.txt', encoding='utf-8')
for line in file.readlines():
    cast_list.append(line.strip())

result = []

for index, row in weibo.iterrows():
    print(index)
    for cast in cast_list:
        if cast in row['content']:
            result.append({'weibo_id': row['weibo_id'], 'content': row['content'], 'time': row['time']})
            break

df = pd.DataFrame(result, columns=['weibo_id', 'content', 'time'])
df.to_csv('../../input/weibo_filtered.csv', index=False, encoding='utf-8')

# -*- coding:utf-8 -*-
"""
抽取福布斯排行榜特征构建画像
"""
import pandas as pd

_2011 = pd.read_csv('../input/2011.csv')
_2012 = pd.read_csv('../input/2012.csv')
_2013 = pd.read_csv('../input/2013.csv')
_2014 = pd.read_csv('../input/2014.csv')
_2015 = pd.read_csv('../input/2015.csv')
_2016 = pd.read_csv('../input/2016.csv')

# df = pd.merge(_2011, _2012, left_on='姓名', right_on='姓名', how='outer')
# df = pd.merge(df, _2013, left_on='姓名', right_on='姓名', how='outer')
# df = pd.merge(df, _2014, left_on='姓名', right_on='姓名', how='outer')
# df = pd.merge(df, _2015, left_on='姓名', right_on='姓名', how='outer')
# df = pd.merge(df, _2016, left_on='姓名', right_on='姓名', how='outer')
#
# df.to_csv('../input/fubusi.csv', index=False, encoding='utf-8')

cast = dict()

for index, item in _2011.iterrows():
    name = item['姓名']
    income = item['收入（万元）']
    # exposure = 0.2 * item['报纸'] + 0.4 * item['杂志和电视'] + 0.4 * item['网络']

    cast[name] = {'income': income}

for index, item in _2012.iterrows():
    name = item['姓名']
    income = item['收入(万元)']
    # exposure = 0.2 * item['报纸'] + 0.4 * item['杂志和电视'] + 0.4 * item['网络']
    try:
        cast[name] = {'income': (cast[name][income] + income) / 2}
    except KeyError:
        cast[name] = {'income': income}

for index, item in _2013.iterrows():
    name = item['姓名']
    income = item['收入（万元）']
    # exposure = 0.2 * item['报纸'] + 0.4 * item['杂志和电视'] + 0.4 * item['网络']
    try:
        cast[name] = {'income': (cast[name][income] + income) / 2}
    except KeyError:
        cast[name] = {'income': income}

for index, item in _2014.iterrows():
    name = item['姓名']
    income = item['收入（万元）']
    # exposure = 0.2 * item['报纸'] + 0.4 * item['杂志和电视'] + 0.4 * item['网络']
    try:
        cast[name] = {'income': (cast[name][income] + income) / 2}
    except KeyError:
        cast[name] = {'income': income}

for index, item in _2015.iterrows():
    name = item['姓名']
    income = item['万元']
    # exposure = 0.2 * item['报纸'] + 0.4 * item['杂志和电视'] + 0.4 * item['网络']
    try:
        cast[name] = {'income': (cast[name][income] + income) / 2}
    except KeyError:
        cast[name] = {'income': income}

for index, item in _2016.iterrows():
    name = item['姓名']
    income = item['万元']
    # exposure = 0.2 * item['报纸'] + 0.4 * item['杂志和电视'] + 0.4 * item['网络']
    try:
        cast[name] = {'income': (cast[name][income] + income) / 2}
    except KeyError:
        cast[name] = {'income': income}

result = []
for key in cast.keys():
    result.append({'name': key, 'income': cast[key]['income']})

df = pd.DataFrame(result, columns=['name', 'income'])
df.to_csv('../input/fubusi_portrait.csv', index=False, encoding='utf-8')
print(cast)
